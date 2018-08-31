from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NewsFeed


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")

    class Meta:
        model = User
        fields = ['username', 'url']


class NewsFeedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = '__all__'
        model = NewsFeed
