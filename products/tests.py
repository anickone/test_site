from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
import os
import tempfile
from PIL import Image


path_img = os.path.join(settings.MEDIA_ROOT, 'tests/logo.png')

class CreatePoductTest(TestCase):
    """ Create tests """

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = get_user_model().objects.create_user(
            'test_user1@gmail_.com',
            'test_user1'
        )
        self.client.force_authenticate(self.test_user1)
        image = Image.open(path_img)
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(self.tmp_file)
        self.tmp_file.seek(0)
        self.valid_payload = {
            'name': 'product test',
            'description': 'description product',
            'logo': self.tmp_file
        }
        self.invalid_payload = {
            'name': 'product test',
            'description': '',
            'logo': self.tmp_file
        }

    def test_create_product_valid(self):
        response = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_invalid_no_data(self):
        response = self.client.post(
            reverse('product-list'),
            data=self.invalid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_invalid_no_login_user(self):
        self.client.logout()
        response = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PoductTest(TestCase):
    """ Read, Update, Delete tests """

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = get_user_model().objects.create_user(
            'test_user1@gmail_.com',
            'test_user1'
        )
        self.client.force_authenticate(self.test_user1)
        image = Image.open(path_img)
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(self.tmp_file)
        self.tmp_file.seek(0)
        self.valid_payload = {
            'name': 'product test',
            'description': 'description product',
            'logo': self.tmp_file
        }
        self.invalid_payload = {
            'name': 'product test',
            'description': '',
            'logo': self.tmp_file
        }
        response_post = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='multipart'
        )
        self.product_url = response_post.data['url']

# read
    def test_get_product_valid(self):
        self.client.logout()
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# update
    def test_update_product_valid(self):
        self.tmp_file.seek(0)
        response = self.client.put(
            self.product_url,
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_invalid_not_owner(self):
        self.tmp_file.seek(0)
        self.client.logout()
        self.test_user2 = get_user_model().objects.create_user(
            'test_user2@gmail_.com',
            'test_user2'
        )
        self.client.force_authenticate(self.test_user2)
        response = self.client.put(
            self.product_url,
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_invalid_no_data(self):
        self.tmp_file.seek(0)
        response = self.client.put(
            self.product_url,
            data=self.invalid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_invalid_no_login_user(self):
        self.tmp_file.seek(0)
        self.client.logout()
        response = self.client.put(
            self.product_url,
            data=self.valid_payload,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# delete
    def test_delete_product_valid(self):
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_invalid_no_login_user(self):
        self.client.logout()
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_invalid_not_owner(self):
        self.client.logout()
        self.test_user2 = get_user_model().objects.create_user(
            'test_user2@gmail_.com',
            'test_user2'
        )
        self.client.force_authenticate(self.test_user2)
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
