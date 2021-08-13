from django.core import paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from photo.models import *
from profiles.models import *
from .serializers import *
from photo.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def gallery_info(request, galpk):
    # get , edit and delete a specific gallery by its id
    try:
        gallery_obj = Gallery.objects.get(id=galpk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #   GET
    if request.method == 'GET':
        serializer = GallerySerializer(gallery_obj)
        return Response(serializer.data)
    #   PUT
    elif request.method == 'PUT':
        if (gallery_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CreateGallerySerializer(gallery_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #   DELETE
    elif request.method == 'DELETE':
        if (gallery_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        gallery_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_galleries(request, userpk):
    # get a list of galleries of a specific user given its id
    Paginator = PageNumberPagination()
    Paginator.page_size = 20
    try:
        gallery_list = Gallery.objects.all().filter(
            owner_id=userpk).order_by('-date_create')
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #   GET
    if request.method == 'GET':
        results = Paginator.paginate_queryset(gallery_list, request)
        galleries = GallerySerializer(results, many=True)
        return Paginator.get_paginated_response(
            galleries.data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def gallery_list(request):
    # get list of galleries or create a new one
    Paginator = PageNumberPagination()
    Paginator.page_size = 20
    # GET
    if request.method == 'GET':
        gallery_list = Gallery.objects.all()
        results = Paginator.paginate_queryset(gallery_list, request)
        galleries = GallerySerializer(results, many=True)
        return Paginator.get_paginated_response(
            galleries.data)
    # POST
    elif request.method == 'POST':
        serializer = CreateGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            profile_obj = Profile.objects.get(owner=request.user)
            # increment the count of galleries in the profile of the user by 1
            profile_obj.galleries_count += 1
            profile_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def find_gallery(request):
    # search for a gallery by its title ordered from the oldest
    value = request.query_params.get("title")
    galleries = Gallery.objects.filter(title__icontains=value)\
        .order_by('-date_create')
    serializer = GallerySerializer(galleries, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def gallery_comments_list(request, galpk):
    # get list of comments or create a new one
    #  to a specific gallery given its id
    try:
        gallery_obj = Gallery.objects.get(id=galpk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        comments = gallery_obj.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                gallery=gallery_obj, owner=request.user)
            # increment the count of comments in that gallery by 1
            gallery_obj.count_comments += 1
            gallery_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def gallery_comment(request, galpk, compk):
    # get ,edit and delete a specific comment on a gallery given their ids
    try:
        gallery_obj = Gallery.objects.get(id=galpk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        comment_obj = gallery_obj.comments.get(id=compk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = CommentSerializer(comment_obj)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        if (comment_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #   DELETE
    elif request.method == 'DELETE':
        if (comment_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment_obj.delete()
        # decrement the count of comments in that gallery by 1
        gallery_obj.count_comments -= 1
        gallery_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def gallery_photos(request, galpk):
    # get the photos list in a specific gallery given the gallery id
    try:
        gallery_obj = Gallery.objects.get(id=galpk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        photos = gallery_obj.photos.all()
        serializer = PhotoMetaSerializer(photos, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def photo_galleries(request, phopk):
    # get the list of galleries in which
    # a specific photo is added given the photo id
    try:
        photo_obj = Photo.objects.get(media_id=phopk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        galleries = photo_obj.gallery_photos.all()
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def gallery_photo(request, galpk, phopk):
    # add or remove a specific photo in a specific gallery given their ids
    try:
        gallery_obj = Gallery.objects.get(id=galpk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        photo_obj = Photo.objects.get(media_id=phopk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    photos = gallery_obj.photos.all()
    # put a flag to see whether the photo is already in the gallery or not
    if photo_obj in photos:
        exist = True
    else:
        exist = False
    if request.method == 'POST':
        if (gallery_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        # can't add his own photos , the photo must be public,
        # does not exist in the gallery and
        #  there is limitation to 500 items in the gallery
        if ((photo_obj.owner != request.user) and
                (photo_obj.is_public) and (not exist) and
                ((gallery_obj.total_count) < 500)):
            photo_obj.gallery_photos.add(gallery_obj)
            gallery_obj.photos.add(photo_obj)
            # check if the gallery is empty then put the id
            # of the item added as a primary photo id for this gallery
            if gallery_obj.count_total == 0:
                gallery_obj.primary_photo_id = phopk
            # increment the count of items in that gallery by 1
            if photo_obj.media == 'photo':
                gallery_obj.count_photos += 1
            else:
                gallery_obj.count_videos += 1
            gallery_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    #   DELETE
    elif request.method == 'DELETE':
        if (gallery_obj.owner != request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if exist:
            photo_obj.gallery_photos.remove(gallery_obj)
            gallery_obj.photos.remove(photo_obj)
            # decrement the count of items in that gallery by 1
            if photo_obj.media == 'photo':
                gallery_obj.count_photos -= 1
            else:
                gallery_obj.count_videos -= 1
            # check if the gallery turned to be empty therefore
            #  set the primary photo id with null
            if gallery_obj.count_total == 0:
                gallery_obj.primary_photo_id = None
            gallery_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
