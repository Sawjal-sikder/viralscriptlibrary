from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Package
from .serializers import PackageSerializer

class PackageView(generics.ListCreateAPIView):
    serializer_class = PackageSerializer
    
    def get_queryset(self):
        return Package.objects.filter(is_active=True)
  
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()] 
        return [permissions.AllowAny()]
    
class PackageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  
        return [permissions.AllowAny()]  