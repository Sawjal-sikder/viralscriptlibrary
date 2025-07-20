from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import CustomUser

from django.contrib.auth import get_user_model
from .models import PasswordResetCode
User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from .models import PasswordResetCode
from .tasks import send_email_registration_otp



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="email already exists")]
    )
    phone_number = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="phone number already exists")]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # Set is_active=False during creation
        user = CustomUser.objects.create_user(**validated_data, is_active=False)

        # Generate and email verification code
        active_code = PasswordResetCode.objects.create(user=user)
        message = f"""
            Dear User,
            Thank you for registering with us!
            To complete your registration, please use the following verification code:{active_code.code}
            This code is valid for the next 2 minutes. Please do not share this code with anyone.
            If you did not initiate this request, please ignore this email or contact support.

            Best regards,              
            """
      
        send_email_registration_otp.delay(user.email, message)

        return user



class VerifyActiveCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(email=attrs['email'])
            reset_code = PasswordResetCode.objects.get(user=user, code=attrs['code'], is_used=False)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired verification code.")

        if reset_code.is_expired():
            raise serializers.ValidationError("Verification code has expired.")

        self.user = user
        self.reset_code = reset_code
        return attrs

    def save(self):
        self.user.is_active = True
        self.user.save()
        self.reset_code.is_used = True
        self.reset_code.save()
        return self.user



class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user with this email exists.")
        if user.is_active:
            raise serializers.ValidationError("User is already active.")
        self.user = user
        return value

    def save(self):
        # Create a new verification code
        reset_code = PasswordResetCode.objects.create(user=self.user)

        message = f"""
        Dear User,
        Thank you for registering with us!
        To complete your registration, please use the following verification code: {reset_code.code}
        This code is valid for the next 2 minutes. Please do not share this code with anyone.
        If you did not initiate this request, please ignore this email or contact support.

        Best regards,
        """

        # Corrected line
        send_email_registration_otp.delay(self.user.email, message)

        return self.user




# for forgot password
class PasswordResetCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value

    def save(self):
        self.user = User.objects.get(email=self.validated_data['email'])
        reset_code = PasswordResetCode.objects.create(user=self.user)

        message = f"""
        Dear User,
        We received a request to reset your password.
        Please use the following code to reset your password: {reset_code.code}
        This code is valid for the next 2 minutes. Please do not share this code with anyone.
        If you did not initiate this request, please ignore this email or contact support.

        Best regards,
        """

        send_email_registration_otp.delay(self.user.email, message)

        return self.user




class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            reset_code = PasswordResetCode.objects.get(user=user, code=attrs['code'], is_used=False)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset code.")

        # Optional: check expiry
        if reset_code.is_expired():
            raise serializers.ValidationError("Reset code has expired.")
        
        # Store for view use
        self.user = user
        self.reset_code = reset_code
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password2":"Password fields didn't match."})
        
        try:
            user = User.objects.get(email=attrs['email'])
            reset_code = PasswordResetCode.objects.get(user=user, code=attrs['code'], is_used=False)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset code.")

        if reset_code.is_expired():
            raise serializers.ValidationError("Reset code has expired.")

        self.user = user
        self.reset_code = reset_code
        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        self.reset_code.is_used = True
        self.reset_code.save()




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "New password must be different from the old password."})
        
        # Optional: enforce Django's password validators (e.g. min length, complexity)
        validate_password(data['new_password'], self.context['request'].user)
        
        return data
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'full_name', 'phone_number', 'profile_image']
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance