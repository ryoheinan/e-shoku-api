from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from api.serializers import RoomSerializer


class TestRoomSerializer(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'internalid.auth0', 'testuser', 'Test', '2020-01-01', 'FEMALE', 'test_Secret!')

    def test_input_valid(self):
        """
        RoomSerializerのバリデーション確認（正常系）
        """

        input_data = {
            'hosts': [self.user.id],
            'guests': [],
            'room_title': 'Test Room 1234',
            'description': 'This is a test room',
            'datetime': '2021-08-20T09:28:33+09:00',
            'capacity': 100,
            'topic': 'game,music',
            'invite_code': 5000,
            'is_private': False
        }
        serializer = RoomSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_room_title_is_blank(self):
        """
        RoomSerializerのroom_titleバリデーション確認（異常系）
        """

        input_data = {
            'hosts': [self.user.id],
            'guests': [self.user.id],
            'room_title': '',
            'description': 'This is a test room',
            'datetime': '2021-08-20T09:28:33+09:00',
            'capacity': 0,
            'topic': 'game,music',
            'invite_code': 5000,
            'is_private': False
        }
        serializer = RoomSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(),
                              ['room_title', 'capacity'])
        self.assertCountEqual(
            [str(x) for x in serializer.errors['room_title']],
            ['この項目は空にできません。']
        )
        self.assertRaisesMessage(ValidationError, ['この値は1以上にしてください。'])
