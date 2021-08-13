from django.test import TestCase
from rest_framework.test import APITestCase
from .models import gallery, Comments
from django.urls import reverse
from rest_framework.views import status


# Create your tests here.

class TestModels(TestCase):
    def test_model_str(self):
        gallery_obj = gallery.objects.create(title="New Gallery")
        comment_obj = Comments.objects.create(content="New comment")
        self.assertEqual(str(gallery_obj), "New Gallery")
        self.assertEqual(str(comment_obj), "New comment")


class GalleryListCreateAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('gallery-list')

    def test_create_gallery(self):
        self.assertEquals(
            gallery.objects.count(),
            0
        )
        data = {
            'title': 'title',
            'description': 'description'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            gallery.objects.count(),
            1
        )
        gallery_obj = gallery.objects.first()
        self.assertEquals(
            gallery_obj.title,
            data['title']
        )
        self.assertEquals(
            gallery_obj.description,
            data['description']
        )

    def test_create_gallery_failure(self):
        self.assertEquals(
            gallery.objects.count(),
            0
        )
        data = {
            'description': 'description'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            gallery.objects.count(),
            0
        )

    def test_got_gallery_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        gallery_obj = gallery.objects.all()
        self.assertEqual(gallery_obj.count(), 0)
        print("GET Method status code", response.status_code)


class GalleryInfoAPIViewTest(APITestCase):
    def setUp(self):
        self.gallery = gallery.objects.create(
            title='title2', description='description2')
        self.url = reverse('gallery-info', kwargs={'galpk': self.gallery.id})
        self.gallery_invalid_url = reverse('gallery-info', kwargs={'galpk': 0})

    def test_invalid_gallery(self):
        response = self.client.get(self.gallery_invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_gallery_info(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['id'],
            self.gallery.id
        )
        self.assertEquals(
            data['title'],
            self.gallery.title
        )
        self.assertEquals(
            data['description'],
            self.gallery.description
        )

    def test_update_gallery(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['title'] = 'new_title'
        data['description'] = 'new_description'
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.gallery.refresh_from_db()
        self.assertEquals(
            self.gallery.title,
            data['title']
        )
        self.assertEquals(
            self.gallery.description,
            data['description']
        )

    def test_delete_gallery(self):
        self.assertEquals(
            gallery.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            gallery.objects.count(),
            0
        )


class CommentsListCreateAPIView(APITestCase):
    def setUp(self):
        self.gallery = gallery.objects.create(
            title='title2', description='description2')
        self.url = reverse(
            'gallery-comments-list', kwargs={'galpk': self.gallery.id})

    def test_create_comment(self):
        self.assertEquals(
            Comments.objects.count(),
            0
        )
        data = {
            'content': 'content',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        print("Create comment Method status code", response.status_code)
        self.assertEquals(
            Comments.objects.count(),
            1
        )

    def test_create_comment_failure(self):
        self.assertEquals(
            Comments.objects.count(),
            0
        )
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            Comments.objects.count(),
            0
        )

    def test_get_comments(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )


class CommentsInfoAPIViewTest(APITestCase):
    def setUp(self):
        self.gallery = gallery.objects.create(
            title='title2', description='description2')
        self.comment = self.gallery.comments.create(content='content2')
        self.url = reverse(
            'gallery-comment-info',
            kwargs={'galpk': self.gallery.id, 'compk': self.comment.id})
        self.comment_invalid_url = reverse(
            'gallery-comment-info',
            kwargs={'galpk': self.gallery.id, 'compk': 0})

    def test_invalid_comment(self):
        response = self.client.get(self.comment_invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_details(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['id'],
            self.comment.id
        )
        self.assertEquals(
            data['content'],
            self.comment.content
        )

    def test_update_comment(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['content'] = 'new_content'
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.comment.refresh_from_db()
        self.assertEquals(
            self.comment.content,
            data['content']
        )

    def test_delete_comment(self):
        self.assertEquals(
            Comments.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Comments.objects.count(),
            0
        )


'''
    def test_get_gallery_list(self):
        comment = Comments(content='content')
        comment.save()
        gallery_obj = gallery(title='title1', description='description1')
        gallery_obj.save()
        comment.gallery.add(comment)

        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['title'],
            gallery_obj.title
        )
        self.assertEquals(
            data['description'],
            gallery_obj.description
        )
        self.assertEquals(
            data['comments'][0]['content'],
            comment.content
        )
'''
