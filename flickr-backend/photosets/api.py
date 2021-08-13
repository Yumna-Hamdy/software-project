from .models import sets
from .models import commentss
from .serializer import sets_serializer
from .serializer import comments_serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from django import forms
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsOwner
from django.contrib.auth.decorators import permission_required



class RespondPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1


@api_view(['GET'])
def set_lists(request):
    all_sets = sets.objects.all()
    photosets = sets_serializer(all_sets, many=True).data 
    return Response({'photosets': photosets})

@api_view(['GET'])
def get_lists(request, id):
    try:

        get_list = sets.objects.all().filter(owner_id=id)
        
    except:
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    #  for pagination
    Paginator = RespondPagination()
    results = Paginator.paginate_queryset(get_list, request)
    photosets = sets_serializer(results, many=True).data
    return Paginator.get_paginated_response({'photosets': photosets})


@api_view(['POST'])   
@permission_classes((IsAuthenticated,))
def create_set(request):
    if request.method == 'POST':
        serializer = sets_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_set(request, id):
    try:
        get_list = sets.objects.get(id=id)
        if (get_list.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this photoset'},
                 status=status.HTTP_403_FORBIDDEN)
        get_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_meta(request, id):
    try:
        get_list = sets.objects.get(id=id)
        if (get_list.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this photoset'},
                 status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
            serializer = sets_serializer(get_list, data=request.data)
            if serializer.is_valid():
                
                serializer.save()
            
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_comment(request, id):
    try:
        get_list = sets.objects.get(id=id)
        if (get_list.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this photoset'},
                 status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST':
            serializer = comments_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sets=get_list)
                get_list.count_comments += 1
                get_list.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_comment(request, id):
    try:
        get_list = commentss.objects.get(id=id)
        if (get_list.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this photoset'},
                 status=status.HTTP_403_FORBIDDEN)
        get_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_comment(request, id):
    try:
        get_list = commentss.objects.get(id=id)
        if (get_list.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this photoset'},
                 status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
            
            serializer = comments_serializer(get_list, data=request.data)            
            
            if serializer.is_valid():
               
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_comments_list(request, id):
    try:
        #   get_id = sets.id
        get_list = sets.objects.get(id=id)
        #   set_list  =  commentss.objects.all().prefetch_related('sets')
    except:
    
        return Response(status=status.HTTP_404_NOT_FOUND)    
    set_list = get_list.comment.all()
    
    comments = comments_serializer(set_list, many=True).data
    # if comments == []:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    #   comments = comments_serializer(get_list).data 
    return Response({'comments': comments}, status=status.HTTP_200_OK)

    



     
