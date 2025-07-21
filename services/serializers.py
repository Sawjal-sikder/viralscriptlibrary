from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

    def validate(self, data):
        # Check if required price fields are provided
        monthly_price = data.get("regular_price_per_month")
        yearly_price = data.get("regular_price_per_year")
        
        if monthly_price is None or yearly_price is None:
            raise serializers.ValidationError("Both regular_price_per_month and regular_price_per_year are required.")
        
        # Validate that prices are positive numbers
        try:
            if float(monthly_price) <= 0 or float(yearly_price) <= 0:
                raise serializers.ValidationError("Prices must be positive values.")
        except (TypeError, ValueError):
            raise serializers.ValidationError("Prices must be valid numeric values.")
        
        # Validate that title is provided and not empty
        title = data.get("title")
        if not title or title.strip() == "":
            raise serializers.ValidationError("Package title is required.")
        
        return data

    def create(self, validated_data):
        package = Package.objects.create(**validated_data)
        from .utitls import create_stripe_product_and_prices

        try:
            create_stripe_product_and_prices(package)
        except Exception as e:
            raise serializers.ValidationError({"stripe": str(e)})

        return package
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Stripe product and prices
        from .utitls import create_stripe_product_and_prices
        try:
            create_stripe_product_and_prices(instance)
        except Exception as e:
            raise serializers.ValidationError({"stripe": str(e)})

        return instance

