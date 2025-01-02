from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import User
from api.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling User operations
    
    Provides CRUD operations for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow user registration without authentication
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()