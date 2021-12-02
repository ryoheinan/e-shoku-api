from django.test import TestCase
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer


class TestUserSerializer(TestCase):
    def test_input_valid(self):
        """
        UserSerializerのバリデーション確認（正常系）
        """

        input_data = {
            'internal_id': 'internalid.auth0',
            'username': 'testuser',
            'display_name': 'Test San',
            'date_of_birth': '2020-01-01',
            'gender': 'FEMALE',
            'password': 'test_Secret!'
        }
        serializer = UserSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_input_valid_if_is_info_filled_is_true(self):
        """
        UserSerializerのis_info_filledの更新確認（正常系）
        """

        input_data = {
            'internal_id': 'internalid.auth0',
            'username': 'testuser',
            'display_name': 'Test San',
            'date_of_birth': '2020-01-01',
            'gender': 'FEMALE',
        }
        user = get_user_model().objects.create_user(
            'internalid.auth0', 'testuser', 'New Test San', '2020-01-01', 'FEMALE'
        )
        serializer = UserSerializer(instance=user, data=input_data)
        serializer.is_valid()
        save_result = serializer.save()
        self.assertEqual(save_result.is_info_filled, True)

    def test_input_invalid_if_username_is_blank(self):
        """
        UserSerializerのusernameバリデーション確認（異常系）
        """

        input_data = {
            'internal_id': 'internalid.auth0',
            'username': '',
            'display_name': 'Test San',
            'date_of_birth': '2020-01-01',
            'gender': 'FEMALE',
            'password': 'test_Secret!'
        }
        serializer = UserSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['username'])
        self.assertCountEqual(
            [str(x) for x in serializer.errors['username']],
            ['この項目は空にできません。']
        )

    def test_input_invalid_if_gender_is_unknown_data(self):
        """
        UserSerializerのgenderバリデーション確認（異常系）
        """

        input_data = {
            'internal_id': 'internalid.auth0',
            'username': 'testuser',
            'display_name': 'Test San',
            'date_of_birth': '2020-01-01',
            'gender': 'UNKNOWN',
            'image_url': 'test_user.profile.example.com',
            'password': 'test_Secret!'
        }
        serializer = UserSerializer(data=input_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(),
                              ['gender', 'image_url'])
        self.assertCountEqual(
            [str(x) for x in serializer.errors['gender']],
            ['"UNKNOWN"は有効な選択肢ではありません。']
        )
        self.assertCountEqual(
            [str(x) for x in serializer.errors['image_url']],
            ['有効なURLを入力してください。']
        )

    def test_output_data(self):
        """
        UserSerializer出力データの内容検証
        """

        user = get_user_model().objects.create_user(
            'internalid.auth0', 'testuser', 'Test San', '2020-01-01', 'FEMALE'
        )
        serializer = UserSerializer(instance=user)
        expected_data = {
            'id': str(user.id),
            'internal_id': 'internalid.auth0',
            'username': 'testuser',
            'display_name': 'Test San',
            'date_of_birth': '2020-01-01',
            'gender': 'FEMALE',
            'description': None,
            'image_url': None,
            'is_info_filled': False,
        }
        self.assertDictEqual(serializer.data, expected_data)
