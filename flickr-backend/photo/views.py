from .models import *
from accounts.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import os
import datetime

from rest_framework.permissions import IsAuthenticated
from project.permissions import IsOwner
from django.contrib.auth.decorators import permission_required

# Create your views here.


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_perms(request, id):

    try:
        required_photo = Photo.objects.get(media_id=id)

        if (required_photo.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to get'
                             ' perms for this photo'},
                 status=status.HTTP_403_FORBIDDEN)

        photo_perms = PhotoPermSerializer(required_photo).data
        return Response(
            {'stat': 'ok', 'perms': photo_perms}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(
            {'stat': 'fail', 'message': 'Photo not found or invalid photo ID'},
            status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def set_meta(request, id):

    if request.data == {}:
        return Response(
            {'stat': 'fail',
             'message': 'At least a title or a description must be provided'},
            status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            required_photo = Photo.objects.get(media_id=id)

            if (required_photo.owner != request.user):
                return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to set'
                             ' meta for this photo'},
                 status=status.HTTP_403_FORBIDDEN)

            photo_meta = PhotoMetaSerializer(
                instance=required_photo, data=request.data)
            if photo_meta.is_valid():
                #   Ensures that title field has no more than 300 characters
                #   and description no more than 2000
                photo_meta.save()
                return Response(
                    {'stat': 'ok', 'photo': photo_meta.data},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'stat': 'fail', 'message': photo_meta.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {'stat': 'fail',
                 'message': 'Photo not found or invalid photo ID'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def set_dates(request, id):

    if request.data == {}:
        return Response(
            {'stat': 'fail',
             'message': 'Missing requirements.'
             'At least one date must be provided'},
            status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            required_photo = Photo.objects.get(media_id=id)

            if (required_photo.owner != request.user):
                return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to set'
                             ' dates this photo'},
                 status=status.HTTP_403_FORBIDDEN)

            photo_dates = PhotoDatesSerializer(
                instance=required_photo, data=request.data)

            if photo_dates.is_valid():

                #   Detects whether DateTime format is invalid

                for date in request.data:
                    if ((request.data[date] < '1970-01-01T00:00:00-05:00') or
                       (request.data[date] > str(datetime.datetime.now()))):
                        return Response(
                            {'stat': 'fail',
                             'message': 'Date posted or date taken is '
                             'in the future or way in the past'},
                            status=status.HTTP_400_BAD_REQUEST)

                if (len(request.data) == 2 and
                   request.data['date_taken'] >= request.data['date_posted']):
                    return Response({'stat': 'fail',
                                     'message': 'Date taken should be '
                                     'before date posted'},
                                    status=status.HTTP_400_BAD_REQUEST)

            #   date_posted cannot be null
            #   beacuse it is always set at uploading
                if (len(request.data) == 1
                    and list(request.data.keys())[0] == 'date_taken'
                   and request.data['date_taken']
                   >= str(required_photo.date_posted)):
                    return Response({'stat': 'fail',
                                     'message': 'Date taken should be '
                                     'before date posted'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if (len(request.data) == 1
                    and list(request.data.keys())[0] == 'date_posted'
                   and required_photo.date_taken is not None
                   and request.data['date_posted']
                   <= str(required_photo.date_taken)):
                    return Response({'stat': 'fail',
                                     'message': 'Date taken should be '
                                     'before date posted'},
                                    status=status.HTTP_400_BAD_REQUEST)

                photo_dates.save()
                return Response({'stat': 'ok',
                                 'photo': photo_dates.data},
                                status=status.HTTP_200_OK)

            else:
                return Response({'stat': 'fail',
                                 'message': photo_dates.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'Photo not found'
                             'or invalid photo ID'},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def edit_or_delete_comment(request, id):

    try:
        required_comment = Comment.objects.get(comment_id=id)

        if (required_comment.owner != request.user):
            return Response(
                {'stat': 'fail',
                 'message': 'User does not have permission to edit'
                            ' or delete this comment'},
                status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PUT':

            if request.data == {}:
                return Response({'stat': 'fail',
                                 'message': 'Blank Comment'},
                                status=status.HTTP_400_BAD_REQUEST)

            edited_comment = PhotoCommentSerializer(instance=required_comment,
                                                    data=request.data)

            author_id = required_comment.author_id
            author = Account.objects.get(id=author_id)
            author_username = author.username
            author_email = author.email
            author_data = {'author_id': author_id,
                           'author_username': author_username,
                           'author_email': author_email}

            photo_id = required_comment.photo_id

            if edited_comment.is_valid():

                #   Ensures that comment_text field
                #   has no more than 1000 characters

                edited_comment.save()
                return Response({'stat': 'ok', 'photo_id': photo_id,
                                 'comment': edited_comment.data,
                                 'author_data': author_data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'stat': 'fail',
                                 'message': edited_comment.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            required_comment.delete()
            return Response({'stat': 'ok'}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'stat': 'fail',
                         'message': 'Comment not found'
                         'or invalid comment ID'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def edit_or_delete_note(request, id):

    try:
        required_note = Note.objects.get(note_id=id)

        if (required_note.owner != request.user):
            return Response(
                {'stat': 'fail',
                 'message': 'User does not have permission to edit'
                            ' or delete this note'},
                status=status.HTTP_403_FORBIDDEN)

        if request.method == 'PUT':

            if ('left_coord' not in request.data
                or 'top_coord' not in request.data
                or 'note_width' not in request.data
                or 'note_height' not in request.data
               or 'note_text' not in request.data):

                return Response({'stat': 'fail',
                                 'message': 'Missing required arguments'},
                                status=status.HTTP_400_BAD_REQUEST)

            edited_note = PhotoNoteSerializer(instance=required_note,
                                              data=request.data)

            author_id = required_note.author_id
            author = Account.objects.get(id=author_id)
            author_username = author.username
            author_email = author.email
            author_data = {'author_id': author_id,
                           'author_username': author_username,
                           'author_email': author_email}

            photo_id = required_note.photo_id
            photo = Photo.objects.get(media_id=photo_id)
            displaypx = photo.photo_displaypx

            left_coord = request.data['left_coord']
            top_coord = request.data['top_coord']
            note_width = request.data['note_width']
            note_height = request.data['note_height']

            if edited_note.is_valid():
                #   Detects whether a string is inserted in an integer field
                #   or a negative integer is entered or a float is entered
                #   Ensures that note_text field has no more
                #   than 1000 characters

                if ((int(left_coord) <= int(displaypx))
                    and (int(top_coord) <= 500) and
                    (int(note_width) <= int(displaypx)-int(left_coord))
                   and (int(note_height) <= 500-int(top_coord))):
                    edited_note.save()
                    return Response({'stat': 'ok',
                                     'photo_id': photo_id,
                                     'note': edited_note.data,
                                     'author_data': author_data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'stat': 'fail',
                                     'message': 'Note would exceed'
                                     'photo dimensions'},
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'stat': 'fail',
                                 'message': edited_note.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            required_note.delete()
            return Response({'stat': 'ok'}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'stat': 'fail',
                         'message': 'Note not found'
                         'or invalid note ID'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_photo(request, id):

    try:
        photo_required = Photo.objects.get(media_id=id)

        if (photo_required.owner != request.user):
            return Response(
                {'stat': 'fail',
                 'message': 'User does not have permission to delete'
                            ' this photo'},
                status=status.HTTP_403_FORBIDDEN)

        media_file = photo_required.media_file
        os.remove('media/' + str(media_file))
        photo_required.delete()
        return Response({'stat': 'ok'}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'stat': 'fail',
                         'message': 'Photo not found'
                         ' or invalid photo ID'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_views(request, id):

    try:
        photo_required = Photo.objects.get(media_id=id)
        photo_views = View.objects.filter(
            photo_id=photo_required.media_id).order_by('view_date')
        photo_views_count = View.objects.filter(photo_id=id).count()
        views_objects = PhotoViewSerializer(
            photo_views, many=True).data
        return Response({'stat': 'ok', 'photo_id': id,
                         'views_count': photo_views_count,
                         'views': views_objects},
                        status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'stat': 'fail',
                         'message': 'Photo not found'
                         ' or invalid photo ID'},
                        status=status.HTTP_404_NOT_FOUND)
