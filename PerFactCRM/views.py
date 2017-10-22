from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/crm/index.html'))
        else:
            error_msg = '用户名或者密码错误'

    return render(request, 'login.html', {'error_msg': error_msg})



def user_login_out(request):
    logout(request)
    return redirect('/login.html')