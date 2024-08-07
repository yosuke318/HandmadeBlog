from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Article

from my_blog.forms import ArticleForm


def fetch_users_list(request):
    """
    Topページにてユーザ一覧を表示（確認用）
    :param request:
    :return:
    """
    user = get_user_model()

    users = user.objects.all()

    context = {'users': users}

    return render(request, 'top.html', context)


def register(request):
    """
    ユーザ登録ページにて登録する
    :param request:
    :return:
    """
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('top')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def post_article(request):
    """
    ログインユーザによる記事投稿とhtmlへ記事情報を提供
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('post_article')
    else:
        form = ArticleForm()

    user_posts = Article.objects.filter(author=request.user)

    context = {
        'form': form,
        'posts': user_posts
    }
    return render(request, 'post_article.html', context)


