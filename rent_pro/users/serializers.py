from operator import mod
from users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','is_superuser','is_staff','groups', 'user_permissions',)

class UserGraphSerializer(serializers.ModelSerializer):
    counted = serializers.IntegerField()
    dated = serializers.CharField()
    class Meta:
        model = User
        fields = ['id','date_joined','counted','dated']