from rest_framework import serializers
from .models import *


# Serializers define the API representation.
class PhotoPermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            'media_id', 'is_public', 'is_friend',
            'is_family', 'can_comment', 'can_addmeta']


class PhotoMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['media_id', 'title', 'description']


class PhotoDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['media_id', 'date_taken', 'date_posted']


class PhotoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'date_created', 'comment_text']
        #   fields = ['comment_id', 'date_created', 'comment_text', 'link']


class PhotoNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'note_id', 'left_coord', 'top_coord',
            'note_width', 'note_height', 'note_text']


class PhotoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ['view_date', 'user_id']
