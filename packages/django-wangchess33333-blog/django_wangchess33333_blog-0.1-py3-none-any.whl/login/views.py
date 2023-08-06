# login/views.py

# login/views.py

from collections import UserDict
from django.shortcuts import render,redirect
from .froms import UserForm
from .models import Userpass
from .froms import RegisterForm
# login/views.py



# login/views.py


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = Userpass.objects.get(uname=username)
            pass1= Userpass.objects.get(passwordd=password)
            if user.uname == username:
                if password == pass1.passwordd:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.uname
                    return redirect('/blog/')
                else:
                    message = "密码不正确！"
            else:
                message = "用户名不正确！"

            
            
                
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    else:
       del request.session['is_login']
       del request.session['user_id']
       del request.session['user_name']
       return redirect("/blog/")
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect('/blog/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = Userpass.objects.filter(uname=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = Userpass.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = Userpass.objects.create()
                new_user.uname = username
                new_user.passwordd = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())