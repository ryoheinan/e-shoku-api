from django.test import TestCase
from django.contrib.auth import get_user_model
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
            'room_name': 'Test Room',
            'topic': 'game,music',
            'invite_code': 5000,
            'is_private': False
        }
        serializer = RoomSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_room_name_is_blank(self):
        """
        RoomSerializerのroom_nameバリデーション確認（異常系）
        """

        input_data = {
            'hosts': [self.user.id],
            'guests': [self.user.id],
            'room_name': '',
            'topic': 'game,music',
            'invite_code': 5000,
            'is_private': False
        }
        serializer = RoomSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['room_name'])
        self.assertCountEqual(
            [str(x) for x in serializer.errors['room_name']],
            ['この項目は空にできません。']
        )
