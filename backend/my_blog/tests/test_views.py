from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class IndexTests(TestCase):
    """IndexViewのテストクラス"""

    def setUp(self):
        """テスト環境準備のため、テストユーザを用意"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get(self):
        """URLパターンloginにアクセス"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # ユーザーでログイン(パスワードかユーザ名が一致していないとエラー)
        response = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(response)


class RegistrationTestCase(TestCase):
    def test_registration_view(self):
        # ユーザー登録ページにアクセス
        response = self.client.get(reverse('register'))

        # ページが正常にアクセスできることを確認
        self.assertEqual(response.status_code, 200)

        # ユーザー登録フォームにデータを送信
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })

        # ユーザーが正常に登録されたことを確認
        self.assertEqual(response.status_code, 302)  # リダイレクトされる
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # def test_registration_with_existing_user(self):
    #     # 既存のユーザーを作成
    #     User.objects.create_user(username='existinguser', password='existingpassword')
    #
    #     # 既存のユーザー名でユーザー登録を試みる
    #     response = self.client.post(reverse('register'), {
    #         'username': 'existinguser',
    #         'password1': 'newpassword123',
    #         'password2': 'newpassword123'
    #     })
    #
    #     # ユーザー登録が失敗し、エラーメッセージが表示されることを確認
    #     self.assertEqual(response.status_code, 200)  # ページが再表示される
    #     self.assertContains(response, "A user with that username already exists.")
