import json

from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse
from django.test import TestCase, Client

from rest_framework import status
from rest_framework.test import APITestCase

from .models import *
from .serializers import *
from .views import *
from .urls import *

import datetime

# Create your tests here.


class TestGetPerms(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.valid_url = reverse('photo:get_perms',
                                 kwargs={'id': self.photo.media_id})
        self.invalid_url = reverse('photo:get_perms', kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.get(self.valid_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['perms']['is_public'], True)
        self.assertEqual(response.data['perms']['is_family'], False)
        self.assertEqual(response.data['perms']['is_friend'], False)

        self.assertEqual(response.data['perms']['can_comment'], 3)
        self.assertEqual(response.data['perms']['can_addmeta'], 3)

    def test_invalid_photoID(self):
        response = self.client.get(self.invalid_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSetMeta(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.valid_url = reverse('photo:set_meta',
                                 kwargs={'id': self.photo.media_id})
        self.invalid_url = reverse('photo:set_meta', kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.put(self.valid_url, {'title': 'This is a title',
                                                    'description': 'This is a '
                                                    'description'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['photo']['title'], 'This is a title')
        self.assertEqual(response.data['photo']['description'],
                         'This is a description')

    def test_blank_body(self):
        response = self.client.put(self.valid_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "At least a title or "
                                         "a description must be provided"})

    def test_exceeding_characters(self):
        response = self.client.put(self.valid_url, {'title': 'This is a title.'
                                                    'This is a title.This is a'
                                                    'title.This is a title.Thi'
                                                    's is a title.This is a ti'
                                                    'tle.This is a title.This '
                                                    'is a title.This is a titl'
                                                    'e.This is a title.This is'
                                                    ' a title.This is a title.'
                                                    'This is a title.This is a'
                                                    ' title.This is a title.Th'
                                                    'is is a title.This is a t'
                                                    'itle.This is a title.This'
                                                    ' is a title.'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         {"title":
                                          ["Ensure this field has no more "
                                           "than 300 characters."]}})

    def test_invalid_photoID(self):
        response = self.client.put(self.invalid_url, {'title': 'This is'
                                                      ' a title',
                                                      'description': 'This is '
                                                      'a description'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSetDates(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          date_taken='2021-04-05T05:00:00Z',
                                          media='Photo',
                                          media_file='media/images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.valid_url = reverse('photo:set_dates',
                                 kwargs={'id': self.photo.media_id})
        self.invalid_url = reverse('photo:set_dates', kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.put(self.valid_url, {'date_taken': '2021-02-01'
                                                    'T05:00:00Z',
                                                    'date_posted': '2021-02-02'
                                                    'T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['photo']['date_taken'],
                         '2021-02-01T05:00:00Z')
        self.assertEqual(response.data['photo']['date_posted'],
                         '2021-02-02T05:00:00Z')

    def test_blank_body(self):
        response = self.client.put(self.valid_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Missing requirements."
                                         "At least one date must be provided"})

    def test_too_old_date(self):
        response = self.client.put(self.valid_url, {'date_taken':
                                                    '1800-02-01T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Date posted or date taken"
                                         " is in the future "
                                         "or way in the past"})

    def test_future_date(self):
        response = self.client.put(self.valid_url, {'date_taken': '2022-02-01'
                                                    'T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Date posted or date "
                                         "taken is in the future "
                                         "or way in the past"})

    def test_date_posted_before_taken_both_passed(self):
        response = self.client.put(self.valid_url, {'date_taken': '2021-02-01'
                                                    'T05:00:00Z',
                                                    'date_posted': '2020-02-02'
                                                    'T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Date taken should be "
                                         "before date posted"})

    def test_date_posted_before_taken_date_posted_passed(self):
        response = self.client.put(self.valid_url, {'date_posted': '2020-02-02'
                                                    'T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Date taken should be "
                                         "before date posted"})

    def test_date_posted_before_taken_date_taken_passed(self):
        response = self.client.put(self.valid_url, {'date_taken': '2021-04-07'
                                                    'T05:00:00Z'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Date taken should be "
                                         "before date posted"})

    def test_invalid_date_format(self):
        response = self.client.put(self.valid_url, {'date_taken': '21-2-2000'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         {"date_taken": ["Datetime has wrong "
                                                         "format. Use one of"
                                                         " these formats "
                                                         "instead: YYYY-MM-DD"
                                                         "Thh:mm[:ss[.uuuuuu]]"
                                                         "[+HH:MM|-HH:MM|Z]"
                                                         "."]}})

    def test_invalid_photoID(self):
        response = self.client.put(self.invalid_url, {
            'date_taken': '2021-02-01T05:00:00Z',
            'date_posted': '2021-02-02T05:00:00Z'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestEditComment(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.comment = Comment.objects.create(author=self.user,
                                              comment_text='This is a comment',
                                              photo=self.photo)
        self.valid_url = reverse('photo:edit_or_delete_comment',
                                 kwargs={'id': self.comment.comment_id})
        self.invalid_url = reverse('photo:edit_or_delete_comment',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.put(self.valid_url,
                                   {'comment_text':
                                    'This is an edited comment'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment']['comment_text'],
                         'This is an edited comment')

        self.assertEqual(response.data['author_data']['author_username'],
                         'sandra_adel')
        self.assertEqual(response.data['author_data']['author_email'],
                         'sandra99@yahoo.com')

    def test_blank_body(self):
        response = self.client.put(self.valid_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message": "Blank Comment"})

    def test_exceeding_characters(self):
        response = self.client.put(self.valid_url, {'comment_text':
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'
                                                    'This is a comment.'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         {"comment_text":
                                          ["Ensure this field has no more "
                                           "than 1000 characters."]}})

    def test_invalid_commentID(self):
        response = self.client.put(self.invalid_url, {'comment_text':
                                                      'This is a comment'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteComment(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06'
                                                      'T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.comment = Comment.objects.create(author=self.user,
                                              comment_text='This is a comment',
                                              photo=self.photo)
        self.valid_url = reverse('photo:edit_or_delete_comment',
                                 kwargs={'id': self.comment.comment_id})
        self.invalid_url = reverse('photo:edit_or_delete_comment',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'stat': 'ok'})

    def test_invalid_commentID(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestEditNote(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06'
                                                      'T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.note = Note.objects.create(author=self.user, left_coord=0,
                                        top_coord=0, note_width=50,
                                        note_height=50,
                                        note_text='This is a note',
                                        photo=self.photo)
        self.valid_url = reverse('photo:edit_or_delete_note',
                                 kwargs={'id': self.note.note_id})
        self.invalid_url = reverse('photo:edit_or_delete_note',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.put(self.valid_url, {'left_coord': 50,
                                                    'top_coord': 50,
                                                    'note_width': 100,
                                                    'note_height': 100,
                                                    'note_text':
                                                    'This is an edited note'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['note']['note_text'],
                         'This is an edited note')

        self.assertEqual(response.data['note']['left_coord'], 50)
        self.assertEqual(response.data['note']['top_coord'], 50)
        self.assertEqual(response.data['note']['note_width'], 100)
        self.assertEqual(response.data['note']['note_height'], 100)

        self.assertEqual(response.data['author_data']['author_username'],
                         'sandra_adel')
        self.assertEqual(response.data['author_data']['author_email'],
                         'sandra99@yahoo.com')

    def test_missing_arguments(self):
        response = self.client.put(self.valid_url,
                                   {'note_text': 'This is an edited note'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         "Missing required arguments"})

    def test_note_exceeding_photo_dimensions(self):
        response = self.client.put(self.valid_url, {'left_coord': 300,
                                                    'top_coord': 500,
                                                    'note_width': 50,
                                                    'note_height': 50,
                                                    'note_text':
                                                    'This is an edited note'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail", "message":
                                         "Note would exceed"
                                         "photo dimensions"})

    def test_negative_value_passed(self):
        response = self.client.put(self.valid_url, {'left_coord': -1,
                                                    'top_coord': 50,
                                                    'note_width': 100,
                                                    'note_height': 100,
                                                    'note_text':
                                                    'This is an edited note'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail", "message":
                                         {"left_coord": ["Ensure this value"
                                          " is greater than or equal to 0."]}})

    def test_invalid_integer_passed(self):
        response = self.client.put(self.valid_url, {'left_coord':
                                                    'left coordinate',
                                                    'top_coord': 50,
                                                    'note_width': 100,
                                                    'note_height': 100,
                                                    'note_text':
                                                    'This is an edited note'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         {"left_coord": ["A valid integer"
                                          " is required."]}})

    def test_exceeding_characters(self):
        response = self.client.put(self.valid_url, {'left_coord': 50,
                                                    'top_coord': 50,
                                                    'note_width': 100,
                                                    'note_height': 100,
                                                    'note_text':
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'
                                                    'This is an edited note.'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"stat": "fail",
                                         "message":
                                         {"note_text": ["Ensure this field"
                                          " has no more than 1000 characters."
                                                        ]}})

    def test_invalid_noteID(self):
        response = self.client.put(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteNote(APITestCase):

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.note = Note.objects.create(author=self.user, left_coord=0,
                                        top_coord=0, note_width=50,
                                        note_height=50,
                                        note_text='This is a note',
                                        photo=self.photo)
        self.valid_url = reverse('photo:edit_or_delete_note',
                                 kwargs={'id': self.note.note_id})
        self.invalid_url = reverse('photo:edit_or_delete_note',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'stat': 'ok'})

    def test_invalid_noteID(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeletePhoto(APITestCase):

    #   Take care dummy_photo.jpg has to be there in images_and_videos
    #   folder in media folder before running the test

    def setUp(self):
        self.user = Account.objects.create(username='sandra_adel',
                                           email='sandra99@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.valid_url = reverse('photo:delete_photo',
                                 kwargs={'id': self.photo.media_id})
        self.invalid_url = reverse('photo:delete_photo',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'stat': 'ok'})

    def test_invalid_photoID(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGetViews(APITestCase):

    def setUp(self):
        self.user1 = Account.objects.create(username='sandra_adel',
                                            email='sandra99@yahoo.com')
        self.user2 = Account.objects.create(username='tim_walkers',
                                            email='tim22@yahoo.com')
        self.user3 = Account.objects.create(username='peter_adams',
                                            email='peter33@yahoo.com')
        self.photo = Photo.objects.create(owner=self.user1,
                                          date_posted='2021-04-06T05:00:00Z',
                                          media='Photo',
                                          media_file='images_and_videos'
                                                     '/dummy_photo.jpg',
                                          photo_displaypx=300,
                                          video_duration=0)
        self.view1 = View.objects.create(user=self.user2,
                                         photo=self.photo)
        self.view2 = View.objects.create(user=self.user3,
                                         photo=self.photo)
        self.valid_url = reverse('photo:get_views',
                                 kwargs={'id': self.photo.media_id})
        self.invalid_url = reverse('photo:get_views',
                                   kwargs={'id': 0})

    def test_normal_case(self):
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views_count'], 2)

    def test_invalid_photoID(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
