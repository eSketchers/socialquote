# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import UserSerializer,UserProfileSerializer,QuoteSerializer
from models import UserProfile,Quote
from django.contrib.auth.models import User
import facebook
import json

class UserView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self,request, format=None):        
        data = request.DATA
        graph = facebook.GraphAPI(data['token'])
        profile = graph.get_object("me")
        picture = graph.get_connections("me", "picture")
        objUser = {}
        objUser['first_name'] = profile['first_name']
        objUser['last_name'] = profile['last_name']
        objUser['email'] = profile['email']
        objUser['username'] = profile['id']
        objUser['is_active'] = True
        objProfile = {}
        objProfile['access_token'] = data['token']
        objProfile['profile_picture'] = picture['url']
        objProfile['gender'] = profile['gender']
        objUser['user_profile'] = objProfile
        user = UserSerializer()
        serializer = UserSerializer(data=objUser)        
        try:
            userobj = User.objects.get(username=objUser['username'])
            return Response(objUser, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            if serializer.is_valid():
                serializer.save()      
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuoteView(APIView):
    def get(self,request, format=None):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes,many=True)
        return Response(serializer.data)
        
    def post(self,request,format=None):
        data = request.DATA['quoteData']        
        user_id = data['user_id']
        try:
            objUser = User.objects.get(username=user_id)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        objQuote = {}
        objQuote['quote_text'] = data['text']
        if data['author']:
            objQuote['quote_author'] = data['author']
        else:
            objQuote['quote_author'] = objUser['first_name']+' '+objUser['last_name']
        if data['tags']:
            objQuote['tags'] = data['tags']        
        objQuote['color'] = data['color']
        objQuote['comments'] = []
        objQuote['likes'] = []  
        objQuote['user'] = objUser
        try:
            serializer = QuoteSerializer(objQuote)
            if serializer.is_valid():
                serializer.save()
#             quote=Quote(user=objUser,quote_text=objQuote['quote_text'],quote_author=objQuote['quote_author'],tags=objQuote['tags'],color=objQuote['color'])
#             quote.save()  
                return Response(objQuote,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)