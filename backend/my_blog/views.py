from django.shortcuts import render
from django.contrib.auth import get_user_model


def fetch_users_list(request):
    user = get_user_model()

    users = user.objects.all()

    context = {'users': users}

    return render(request, 'top.html', context)

