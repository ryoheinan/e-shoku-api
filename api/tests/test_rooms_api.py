from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import Room


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
            'description': 'This is a test room',
            'datetime': '2021-08-20T09:28:33+09:00',
            'capacity': 100,
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
        self.other_user = get_user_model().objects.create_user(
            'internalid_tmp.auth0', 'other_user', 'other_user', '2020-01-01', 'FEMALE', 'test_Secret!')

    def test_users_post(self):
        """
        認証ありのPOST検証（正常系）
        """
        data = {
            'hosts': [self.user.id],
            'guests': [self.user.id],
            'room_name': 'Test Room',
            'description': 'This is a test room',
            'datetime': '2021-08-20T09:28:33+09:00',
            'capacity': 100,
            'topic': 'game,music',
            'is_private': False
        }
        res = self.client.post(ROOMS_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().room_name, 'Test Room')
        data['invite_code'] = None
        data['id'] = res.data['id']
        data['created_at'] = res.data['created_at']
        self.assertDictEqual(res.data, data)
        res = self.client.delete(f"{ROOMS_URL}{Room.objects.get().id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), 0)

    def test_users_unauthorized(self):
        """
        他ユーザーアクセス時のPATCH・DELETE検証（異常系）
        """

        other_user_room = Room.objects.create(
            room_name='Test Room',
            description='This is a test room',
            datetime='2021-08-20T09:28:33+09:00',
            capacity=100,
            topic='game,music',
        )
        other_user_room.hosts.add(self.other_user)
        data = {
            'room_name': 'New!! Test Room',
        }
        res = self.client.patch(f"{ROOMS_URL}{other_user_room.id}/", data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.delete(f"{ROOMS_URL}{other_user_room.id}/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Room.objects.count(), 1)

    def test_join_and_leave_room(self):
        """
        認証ありのPOST検証（正常系）
        """

        room = Room.objects.create(
            room_name='Test Room',
            description='This is a test room',
            datetime='2021-08-20T09:28:33+09:00',
            capacity=100,
            topic='game,music',
        )
        user_data = {
            "id": self.user.id,
        }
        other_user_data = {
            "id": self.other_user.id,
        }
        res = self.client.post(f"{ROOMS_URL}join/{room.id}/", user_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(Room.objects.get(guests=self.user.id))
        # 同じユーザーが2回以上参加しようとするとエラー
        res = self.client.post(f"{ROOMS_URL}join/{room.id}/", user_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # 他のユーザーが参加しようとするとエラー
        res = self.client.post(f"{ROOMS_URL}join/{room.id}/", other_user_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 参加キャンセルのテスト
        res = self.client.post(f"{ROOMS_URL}leave/{room.id}/", user_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Room.objects.get().guests.count(), 0)
        # 参加していないユーザーがキャンセルしようとするとエラー
        res = self.client.post(f"{ROOMS_URL}leave/{room.id}/", user_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # 他のユーザーがキャンセルしようとするとエラー
        res = self.client.post(f"{ROOMS_URL}leave/{room.id}/", other_user_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
