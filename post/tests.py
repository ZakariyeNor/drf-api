from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post

class PostAPITests(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass456')

        # Create a post owned by user1
        self.post1 = Post.objects.create(owner=self.user1, title='First Post', content='Content 1')

        # URLs
        self.list_url = '/post/'          # Adjust if your router/path is different
        self.detail_url = f'/post/{self.post1.id}/'

    def test_list_post(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post1.title)

    def test_create_post_authenticated(self):
        self.client.login(username='user2', password='pass456')
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')
        self.assertEqual(response.data['owner'], self.user2.id)

    def test_create_post_unauthenticated(self):
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)

    def test_update_post_owner(self):
        self.client.login(username='user1', password='pass123')
        data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_update_post_not_owner(self):
        self.client.login(username='user2', password='pass456')
        data = {'title': 'Hacked Title', 'content': 'Hacked Content'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_owner(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    def test_delete_post_not_owner(self):
        self.client.login(username='user2', password='pass456')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
