from django.test import TestCase
from django.urls import resolve
from api.views import UserAPIView, RoomListCreateAPIView


class TestRouting(TestCase):

    def test_users_url(self):
        """
        Users APIのルーティング検証
        """

        view = resolve('/api/users/')
        self.assertEqual(view.func.view_class, UserAPIView)

    def test_room_url(self):
        """
        Rooms APIのルーティング検証
        """

        view = resolve('/api/rooms/')
        self.assertEqual(view.func.view_class, RoomListCreateAPIView)
