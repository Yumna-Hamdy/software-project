from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.test import TestCase, Client
# from django.urls import reverse
from .serializers import group_serializer
from .models import group, topic, reply
from rest_framework.reverse import reverse


# Create your tests here.
client = APIClient()


class test_groups(APITestCase):

    def setUp(self):
        self.group = group.objects.create(name="group_test0", privacy=2)

        self.post_group_url = reverse('group_create')
        self.group_valid_url = reverse('group_info',
                                       kwargs={'id': self.group.id})
        self.group_invalid_url = reverse('group_info', kwargs={'id': 0})

    def test_post_group(self):
        data = {"name": "group_test1", "privacy": "1", "eighteenplus": "True"}
        response = self.client.post(self.post_group_url, data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_missing_parameter_group(self):
        data = {"name": "group_test01"}
        response = self.client.post(self.post_group_url, data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_group(self):
        get_response = self.client.get(self.group_valid_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get_group_invalid(self):
        get_response = self.client.get(self.group_invalid_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)


class test_topics(APITestCase):

    def setUp(self):
        self.group = group.objects.create(name="group_test2", privacy=1)
        self.topic = topic.objects.create(subject="topic_test1",
                                          message="topic_test1",
                                          group=self.group)
        self.topic2 = topic.objects.create(subject="topic_test2",
                                           message="topic_test2",
                                           group=self.group)

        self.topic_valid_url = reverse('topic',
                                       kwargs={'group_id': self.group.id})
        self.topic_invalid_url = reverse('topic', kwargs={'group_id': 0})

        self.topics_valid_url = reverse('topic_info',
                                        kwargs={'group_id': self.group.id,
                                                'topic_id': self.topic.id})
        self.topics_invalid_url = reverse('topic_info',
                                          kwargs={'group_id': self.group.id,
                                                  'topic_id': 0})

    def test_post_topic(self):
        topic_data = {"subject": "topic_test", "message": "topic_message"}
        post_topic_response = self.client.post(self.topic_valid_url,
                                               topic_data, format='json')
        self.assertEqual(post_topic_response.status_code,
                         status.HTTP_201_CREATED)

    def test_post_missing_parameter_topic(self):
        topic_data = {"subject": "topic_test"}
        post_topic_response = self.client.post(self.topic_valid_url,
                                               topic_data, format='json')
        self.assertEqual(post_topic_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_get_topic(self):
        topic_get_response = self.client.get(self.topics_valid_url,
                                             format='json')
        self.assertEqual(topic_get_response.status_code, status.HTTP_200_OK)

    def test_get_invalid_topic(self):
        topic_get_response = self.client.get(self.topics_invalid_url,
                                             format='json')
        self.assertEqual(topic_get_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_topics(self):
        topics_get_response = self.client.get(self.topic_valid_url,
                                              format='json')
        self.assertEqual(topics_get_response.status_code, status.HTTP_200_OK)

    def test_get_invalid_topics(self):
        topics_get_response = self.client.get(self.topic_invalid_url,
                                              format='json')
        self.assertEqual(topics_get_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_delete_topics(self):
        delete_topic_response = self.client.delete(self.topics_valid_url,
                                                   format='json')
        self.assertEqual(delete_topic_response.status_code, status.HTTP_200_OK)

    def test_delete_invalid_topics(self):
        delete_topic_response = self.client.delete(self.topics_invalid_url,
                                                   format='json')
        self.assertEqual(delete_topic_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_put_topic(self):
        topic_data = self.client.get(self.topics_valid_url, format='json')
        topic_data = {"subject": "new_topic_test",
                      "message": "new_topic_message"}
        put_topic_response = self.client.put(self.topics_valid_url,
                                             data=topic_data, format='json')
        self.assertEqual(put_topic_response.status_code, status.HTTP_200_OK)

    def test_put_invalid_topic(self):
        topic_data = self.client.get(self.topics_invalid_url,
                                     format='json')
        topic_data = {"subject": "new_topic_test",
                      "message": "new_topic_message"}
        put_topic_response = self.client.put(self.topics_invalid_url,
                                             data=topic_data, format='json')
        self.assertEqual(put_topic_response.status_code,
                         status.HTTP_404_NOT_FOUND)


class test_replies(APITestCase):

    def setUp(self):
        self.group = group.objects.create(name="group_test3", privacy=1)
        self.topic = topic.objects.create(subject="topic_test3",
                                          message="topic_test3",
                                          group=self.group)
        self.reply = reply.objects.create(message="reply_test0",
                                          topic=self.topic)
        self.reply1 = reply.objects.create(message="reply_test1",
                                           topic=self.topic)

        self.reply_valid_url = reverse('reply',
                                       kwargs={'group_id': self.group.id,
                                               'topic_id': self.topic.id})
        self.reply_invalid_url = reverse('reply',
                                         kwargs={'group_id': 0,
                                                 'topic_id': 0})

        self.reply_info_valid_url = reverse('reply_info',
                                            kwargs={'group_id': self.group.id,
                                                    'topic_id': self.topic.id,
                                                    'reply_id': self.reply.id})
        self.reply_info_inval_url = reverse('reply_info',
                                            kwargs={'group_id': self.group.id,
                                                    'topic_id': self.topic.id,
                                                    'reply_id': 0})

    def test_post_reply(self):
        reply_data = {"message": "topic_message"}
        post_reply_response = self.client.post(self.reply_valid_url,
                                               reply_data, format='json')
        self.assertEqual(post_reply_response.status_code,
                         status.HTTP_201_CREATED)

    def test_post_missing_parameter_reply(self):
        reply_data = {}
        post_reply_response = self.client.post(self.reply_valid_url,
                                               reply_data, format='json')
        self.assertEqual(post_reply_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_get_reply(self):
        reply_get_response = self.client.get(self.reply_info_valid_url,
                                             format='json')
        self.assertEqual(reply_get_response.status_code, status.HTTP_200_OK)

    def test_get_invalid_reply(self):
        reply_get_response = self.client.get(self.reply_info_inval_url,
                                             format='json')
        self.assertEqual(reply_get_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_get_replies(self):
        replies_get_response = self.client.get(self.reply_valid_url,
                                               format='json')
        self.assertEqual(replies_get_response.status_code, status.HTTP_200_OK)

    def test_get_invalid_topics(self):
        replies_get_response = self.client.get(self.reply_invalid_url,
                                               format='json')
        self.assertEqual(replies_get_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_delete_reply(self):
        delete_reply_response = self.client.delete(self.reply_info_valid_url,
                                                   format='json')
        self.assertEqual(delete_reply_response.status_code, status.HTTP_200_OK)

    def test_delete_invalid_reply(self):
        delete_reply_response = self.client.delete(self.reply_info_inval_url,
                                                   format='json')
        self.assertEqual(delete_reply_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_put_reply(self):
        reply_data = self.client.get(self.reply_info_valid_url, format='json')
        reply_data = {"message": "new_reply_message"}
        put_reply_response = self.client.put(self.reply_info_valid_url,
                                             data=reply_data, format='json')
        self.assertEqual(put_reply_response.status_code, status.HTTP_200_OK)

    def test_put_invalid_reply(self):
        reply_data = self.client.get(self.reply_info_inval_url,
                                     format='json')
        reply_data = {"message": "new_reply_message"}
        put_reply_response = self.client.put(self.reply_info_inval_url,
                                             data=reply_data, format='json')
        self.assertEqual(put_reply_response.status_code,
                         status.HTTP_404_NOT_FOUND)
