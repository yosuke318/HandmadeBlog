from django.contrib import admin
from django.urls import path, include    # includeを追加でimport
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_blog.urls')),    # appアプリケーションのurls.pyを読み込むように追加
]