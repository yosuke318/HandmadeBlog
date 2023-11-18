from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from my_blog.models import Article


class LoginTests(TestCase):
    """IndexViewのテストクラス"""

    def setUp(self):
        """テスト環境準備のため、テストユーザを用意"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_by_registered_user(self):
        """URLパターンloginにアクセス"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # ユーザーでログイン(パスワードかユーザ名が一致していないとエラー)
        response = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(response)

    def test_get_with_different_password(self):
        """パスワードが一致しないユーザによるログイン確認"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # パスワードが一致しないユーザのログイン
        response = self.client.login(username='testuser', password='paspaspas')  # ログイン結果Falseを返す
        self.assertFalse(response)

    def test_get_with_different_username(self):
        """ユーザ名が一致しないユーザによるログイン確認"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # パスワードが一致しないユーザのログイン
        response = self.client.login(username='gorila', password='testpassword123')  # ログイン結果Falseを返す
        self.assertFalse(response)


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
        self.assertEqual(response.status_code, 302)  # 一時的にリダイレクトされる
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_with_existing_user(self):
        """
        既存のユーザを作成してみる
        :return:
        """
        User.objects.create_user(username='existinguser', password='existingpassword')

        # register関数を用い、既存のユーザー名でユーザー登録を試みる
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })

        # ユーザー登録が失敗し、エラーメッセージが表示される
        self.assertEqual(response.status_code, 200)  # ページが再表示される

        self.assertContains(response, "同じユーザー名が既に登録済みです。")


class PostArticleTestCase(TestCase):
    def setUp(self):
        """
        テスト環境でtest userでログイン
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_post_article(self):
        """
        正常なフォームデータを用意してPOSTリクエスト
        """
        form_data = {'title': 'Test Title', 'content': 'Test Content'}  # 正常データ

        response = self.client.post(reverse('post_article'), data=form_data)  # データ登録

        # 正常終了した場合、一時的にHTTPステータス302が返され、最終的に200が返されることを確認
        self.assertRedirects(response,
                             expected_url='/post_article/',
                             status_code=302,  # 一時的なHTTPステータス
                             target_status_code=200,  # 最終的なHTTPステータス
                             msg_prefix='',
                             fetch_redirect_response=True
                             )

        # リダイレクトされたデータにform_dataに記載されたデータがあるか確認
        redirected_response = self.client.get(response.url)  # リダイレクト先に移動

        self.assertContains(redirected_response, 'Test Title')  # 送信データが含まれているか確認
        self.assertContains(redirected_response, 'Test Content')

        # mirror dbについても確認(mirrorDBのデータはテスト終了後、自動的に削除される。)
        self.assertEqual(Article.objects.count(), 1)  # データが一件追加されているか確認

        first_record = Article.objects.first()  # レコードを取得
        self.assertEqual(first_record.title, 'Test Title')
        self.assertEqual(first_record.content, 'Test Content')
        self.assertEqual(first_record.author, self.user)  # レコード追加したuserのobjectの情報が一致

    def test_post_article_with_invalid_content(self):
        """
        異常なフォームデータを用意してPOSTリクエスト。内部的な機能のバリデーションテスト
        """

        invalid_form_data = {'title': 'test title', 'content': ''}  # contentがない不正なデータ

        response = self.client.post(reverse('post_article'), data=invalid_form_data)  # 不正データ登録

        self.assertEqual(response.status_code, 200)  # フォームが無効なため302へリダイレクトされない

        # フォームエラーが表示されているか確認（日本語ver）
        self.assertFormError(response, 'form', 'contents', 'このフィールドは必須です。')

        self.assertEqual(Article.objects.count(), 0)

    def test_post_article_with_invalid_title(self):
        """
        異常なフォームデータを用意してPOSTリクエスト。内部的な機能のバリデーション機能のテスト
        """

        invalid_form_data = {'title': '', 'content': 'Test Content'}  # contentがない不正なデータ

        response = self.client.post(reverse('post_article'), data=invalid_form_data)  # 不正データ登録

        self.assertEqual(response.status_code, 200)  # フォームが無効なため302へリダイレクトされない

        # フォームエラーが表示されているか確認（日本語ver）
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')

        self.assertEqual(Article.objects.count(), 0)
