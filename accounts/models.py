from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField,EmbeddedModelField

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="user_profile")
    profile_picture = models.CharField(max_length=10000)
    access_token = models.CharField(max_length=1000)
    gender = models.CharField(max_length=10)

class Comment(models.Model):
    user = EmbeddedModelField('User')
    comment_text = models.CharField(max_length=250) 
    date = models.DateTimeField(auto_now_add=True, null=True)
    
class Quote(models.Model):
    user = models.ForeignKey(User)
    quote_text = models.CharField(max_length=401)
    quote_author = models.CharField(max_length=100)
    color = models.CharField(max_length=6)
    tags = ListField()
    comments = ListField(EmbeddedModelField('Comment'))
    likes = ListField()
    date = models.DateTimeField(auto_now_add=True, null=True)
#     