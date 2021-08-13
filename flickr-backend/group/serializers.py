from rest_framework import serializers
from .models import group, role_field, topic, reply
from djongo import models


class group_serializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = '__all__'


class topic_serializer(serializers.ModelSerializer):

    class Meta:
        model = topic
        fields = '__all__'
        extra_kwargs = {'group': {'read_only': True}, 'owner': {'read_only': True}}


class reply_serializer(serializers.ModelSerializer):

    class Meta:
        model = reply
        fields = '__all__'
        extra_kwargs = {'topic': {'read_only': True}, 'owner': {'read_only': True}}
