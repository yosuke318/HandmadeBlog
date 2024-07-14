"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from .views import fetch_users_list, register
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    # ログインとログアウトはdjangoの組み込みメソッドを使用
    path('login/',
         LoginView.as_view(
             redirect_authenticated_user=True,
             template_name='login.html'
         ),
         name='login'),
    path('logout/',
         LogoutView.as_view(
             template_name='logout.html'
         ), name='logout'),
    path('', fetch_users_list, name='top'),
    path('register/', views.register, name='register'),
    path('post_article/', views.post_article, name='post_article'),
]
