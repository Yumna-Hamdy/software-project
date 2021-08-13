from django.test import TestCase
from .models import sets
from .models import commentss
from .serializer import sets_serializer
from .serializer import comments_serializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from . import urls
from . import api


class SetsTestCase(APITestCase):
    def test_create(self):
        data = {"title": "testcase", "description": "test"}
        self.post_set_url = reverse('create_lists')
        response = self.client.post(self.post_set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_missing_parameter(self):
        data = {"title": "testcase"}
        self.post_set_url = reverse('create_lists')
        response = self.client.post(self.post_set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_createcomment(self):
        comment_test = sets.objects.create(title="set_test",
                                           description="test")
        data_id = comment_test.id
        set_url = reverse('create_comment', kwargs={'id': data_id})
        self.assertEqual(commentss.objects.count(), 0)
        data = {"contents": "testcase"}
        response = self.client.post(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(commentss.objects.count(), 1)

    def test_createcomment_missing_parameter(self):
        comment_test = sets.objects.create(title="set_test", 
                                           description="test")
        data_id = comment_test.id
        set_url = reverse('create_comment', kwargs={'id': data_id})
        self.assertEqual(commentss.objects.count(), 0)
        data = {""}
        response = self.client.post(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_editecomment(self):
        comment = commentss.objects.create(contents="testcase")
        data_1 = comment.id
        set_url = reverse('edit_comment', kwargs={'id': data_1})
        data = {"contents": "testcase"}
        response = self.client.put(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editecomment_missing_parameter(self):
        comment = commentss.objects.create(contents="testcase")
        data_1 = comment.id
        set_url = reverse('edit_comment', kwargs={'id': data_1})
        data = {""}
        response = self.client.put(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_editemeta(self):
        set = sets.objects.create(title="set_test", description="test")
        data_1 = set.id
        set_url = reverse('edit_meta', kwargs={'id': data_1})
        data = {"title": "testcase", "description": "test"}
        response = self.client.put(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editemeta_missing_parameter(self):
        set = sets.objects.create(title="set_test", description="test")
        data_1 = set.id
        set_url = reverse('edit_meta', kwargs={'id': data_1})
        data = {"title": "testcase"}
        response = self.client.put(set_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_set(self):
        set = sets.objects.create(title="set_test", description="test")
        data_1 = set.id
        set_url = reverse('delete_lists', kwargs={'id': data_1})
        response = self.client.delete(set_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_set_invalid(self):
        set = sets.objects.create(title="set_test", description="test")
        data_1 = set.id
        set_url = reverse('delete_lists', kwargs={'id': 0})
        response = self.client.delete(set_url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        comment = commentss.objects.create(contents="testcase")
        data_1 = comment.id
        set_url = reverse('delete_comment', kwargs={'id': data_1})
        response = self.client.delete(set_url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_invalid(self):
        comment = commentss.objects.create(contents="testcase")
        data_1 = comment.id
        set_url = reverse('delete_comment', kwargs={'id': 0})
        response = self.client.delete(set_url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getecomment(self):
        comment_test = sets.objects.create(title="set_test",
                                           description="test")
        data_id = comment_test.id
        self.assertEqual(commentss.objects.count(), 0)
        comment = commentss.objects.create(contents="testcase")
        comment.contents = "testcase"
        data_1 = comment.id
        set_url = reverse('get_comment', kwargs={'id': data_id})
        response = self.client.get(set_url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getecomment_invalid(self):
        comment_test = sets.objects.create(title="set_test", 
                                           description="test")
        data_id = comment_test.id
        self.assertEqual(commentss.objects.count(), 0)
        comment = commentss.objects.create(contents="testcase")
        comment.contents = "testcase"
        data_1 = comment.id
        set_url = reverse('get_comment', kwargs={'id': 0})
        response = self.client.get(set_url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_getset(self):
    #     set_test = sets.objects.create(title="set_test", description="test")
    #     data_id = set_test.owner
    #     set_url = reverse('get_lists', kwargs={'owner':" "})
    #     response = self.client.get(set_url,  format= 'json')
    #     self.assertEqual(response.status_code, response.data)

    # def test_getset_invalid(self):
    #     set_test = sets.objects.create(title="set_test", description="test")
    #     data_id = set_test.id
    #     set_url = reverse('get_lists', kwargs={'owner':" "})
    #     response = self.client.get(set_url,  format= 'json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)