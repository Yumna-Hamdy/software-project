from rest_framework import serializers
from .models import sets
from .models import commentss


class sets_serializer(serializers.ModelSerializer):
    class Meta:
        model = sets
        fields = ['id', 'title', 'description', 'date_create', 'date_update',
                  'count_videos',  'count_views', 'count_comments', 
                  'can_comment',
                  'visibility_can_see_set', 'owner', 'primary', 'secret',
                  'server',
                  'farm', 'photos', 'comment']
        depth = 1
        #   extra_kwargs = {'owner': {'read_only': True}}

class setss_serializer(serializers.ModelSerializer):
    class Meta:
        model = sets
        fields = ['title, description']


class comments_serializer(serializers.ModelSerializer):
    class Meta:
        model = commentss
        fields = '__all__'
        extra_kwargs = {'sets': {'read_only': True}}