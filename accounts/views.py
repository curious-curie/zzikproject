from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.shortcuts import redirect
from django import forms

def signup(request):
    if request.method  == 'POST':
        if len(request.POST['password1']) < 6:
            raise forms.ValidationError("Your password should be at least 6 Characters")
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            profile = user.profile
            profile.nickname = request.POST['nickname']
            user.save()
            return redirect('/reviews')
        else:
            messages.error(request,'입력하신 비밀번호가 같은지 다시 한번 확인해주세요')
            #return render_to_response('template_name')
            return render(request, 'accounts/signup.html')


    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/reviews')
        else:
            messages.error(request,'username or password not correct')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/reviews')
