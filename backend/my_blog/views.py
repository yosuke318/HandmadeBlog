
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def fetch_users_list(request):
    user = get_user_model()

    users = user.objects.all()

    context = {'users': users}

    return render(request, 'top.html', context)


def register(request):
    if request.method == 'POST':
        # POSTリクエストの場合、フォームデータを処理
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合、ユーザーを作成しログイン
            user = form.save()
            login(request, user)
            return redirect('top')  # ユーザーをホームページにリダイレクト
    else:
        # GETリクエストの場合、新しいフォームを表示
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

