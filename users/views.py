from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from home.models import PaidUsers
from home.models import Interest


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            reg_user = form.save()
            Interest(user_id=reg_user.id).save()
            PaidUsers(user_id=reg_user).save()
            messages.success(request, 'Account created Successfully! You are now able to login Default news sourcces ins BBC-NEWS and preferred category as Business You Can Change This Later In Your Customize Tab')
            return redirect('login')

    else:
        form = UserRegisterForm()

    register_page = loader.get_template('register.html')
    return HttpResponse(register_page.render({'form': form}, request), )


def check_paid(request):
    check_user = PaidUsers.objects.filter(user_id=request.user).exists()
    if check_user:
        return PaidUsers.objects.get(user_id=request.user)
    else:
        return None




