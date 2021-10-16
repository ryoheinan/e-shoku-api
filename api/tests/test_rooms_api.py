from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


ROOMS_URL = reverse('rooms')


class PublicApiTests(APITestCase):
    """
    認証なしの検証クラス
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'internalid.auth0', 'testuser', 'Test', '2020-01-01', 'FEMALE', 'test_Secret!')
        self.client = APIClient()

    def test_auth_required(self):
        """
        認証なしのPOST検証（異常系）
        """
        data = {
            'hosts': [self.user.id],
            'guests': [],
            'room_name': 'Test Room',
            'topic': 'game,music',
            'is_private': False
        }
        res = self.client.post(ROOMS_URL, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(APITestCase):
    """
    認証ありの検証クラス
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'internalid.auth0', 'testuser', 'Test', '2020-01-01', 'FEMALE', 'test_Secret!')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_users_post(self):
        """
        認証ありのPOST検証（正常系）
        """
        data = {
            'hosts': [self.user.id],
            'guests': [],
            'room_name': 'Test Room',
            'topic': 'game,music',
            'is_private': False
        }
        res = self.client.post(ROOMS_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        # self.assertEqual(get_user_model().objects.get().username, 'testuser')
