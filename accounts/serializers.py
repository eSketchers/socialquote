'''
Created on Sep 24, 2014

@author: apple
'''
from rest_framework import serializers
from models import UserProfile,Quote
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_picture','gender','access_token')


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','is_active','user_profile')
        
class QuoteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Quote
        fields = ('user','quote_text','quote_author','tags','color','comments','likes')
        depth = 1
    
