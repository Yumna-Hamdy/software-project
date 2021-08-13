from .models import group, topic, reply
from .serializers import group_serializer, topic_serializer, reply_serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsOwner
from django.contrib.auth.decorators import permission_required

# Create your views here.


@api_view(['GET'])
def group_info(request, id):

    try:
        group_detail = group.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = group_serializer(group_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def group_create(request):
    serializer = group_serializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['privacy'] == 2:
            serializer.save(invitation_only=True, is_member=True,
                            is_admin=True, is_founder=True)
        else:
            serializer.save(is_member=True, is_admin=True, is_founder=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def topic(request, group_id):

    try:
        group_obj = group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = topic_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group_obj,
                            owner=request.user)
            group_obj.topic_count += 1
            group_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#yomaaaaaaaaaaaaaaaaaa
    elif request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 2

        group_topic = group_obj.group_topic.all()
        result_page = paginator.paginate_queryset(group_topic, request)
        serializer = topic_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def topic_info(request, group_id, topic_id):

    try:
        group_obj = group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        group_topic = group_obj.group_topic.get(id=topic_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = topic_serializer(group_topic)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if (group_topic.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to edit'
                             '  this topic'},
                 status=status.HTTP_403_FORBIDDEN)
        serializer = topic_serializer(group_topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if (group_topic.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this topic'},
                 status=status.HTTP_403_FORBIDDEN)
        operation = group_topic.delete()
        group_obj.topic_count -= 1
        group_obj.save()
        data = {}
        if operation:
            data["stat"] = "ok"
        else:
            data["stat"] = "fail"
        return Response(data=data)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def reply(request, group_id, topic_id):

    try:
        group_detail = group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        group_topic = group_detail.group_topic.get(id=topic_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = reply_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(topic=group_topic, owner=request.user)
            group_topic.count_replies += 1
            group_topic.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 2
        group_topic_reply = group_topic.group_topic_reply.all()
        result_page = paginator.paginate_queryset(group_topic_reply, request)
        serializer = reply_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def reply_info(request, group_id, topic_id, reply_id):

    try:
        group_detail = group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        group_topic = group_detail.group_topic.get(id=topic_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        group_topic_reply = group_topic.group_topic_reply.get(id=reply_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = reply_serializer(group_topic_reply)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if (group_topic_reply.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to edit'
                             '  this reply'},
                 status=status.HTTP_403_FORBIDDEN)
        serializer = reply_serializer(group_topic_reply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if (group_topic_reply.owner != request.user):
            return Response(
                 {'stat': 'fail',
                  'message': 'User does not have permission to delete'
                             '  this reply'},
                 status=status.HTTP_403_FORBIDDEN)
        operation = group_topic_reply.delete()
        group_topic.count_replies -= 1
        group_topic.save()
        data = {}
        if operation:
            data["stat"] = "ok"
        else:
            data["stat"] = "fail"
        return Response(data=data)
