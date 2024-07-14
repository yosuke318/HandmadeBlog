from django.test import TestCase
from django.contrib.auth.models import User


class UserModelTests(TestCase):
    def test_is_empty(self):
        """初期状態だけど1つはデータが存在しているかどうかをチェック (error が期待される)"""
        saved_posts = User.objects.all()
        self.assertEqual(saved_posts.count(), 0)
