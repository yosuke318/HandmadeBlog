from django.db import models


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Articles(models.Model):
    article_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        db_column='user_id',
        blank=False
    )
    contents = models.CharField(max_length=255, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
