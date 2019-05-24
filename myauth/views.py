from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .form import 自定义注册表单,自定义编辑表单,自定义登录表单
from .models import 普通会员表
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='myauth:登录')
def 个人中心(请求):
    内容 = {'用户':请求.user}
    return render(请求, 'myauth/user_center.html',内容)

@login_required(login_url='myauth:登录')
def 编辑个人信息(请求):
    if 请求.method == 'POST':
        编辑表单 = 自定义编辑表单(请求.POST,instance=请求.user)
        if 编辑表单.is_valid():
            编辑表单.save()
            请求.user.普通会员表.昵称 = 编辑表单.cleaned_data['昵称']
            请求.user.普通会员表.生日 = 编辑表单.cleaned_data['生日']
            请求.user.普通会员表.save()
            # 普通会员表(用户=用户, 昵称=编辑表单.cleaned_data['昵称'], 生日=编辑表单.cleaned_data['生日']).save()
            return redirect("myauth:个人中心")

    else:
        编辑表单 = 自定义编辑表单(instance=请求.user)

    内容 = {'编辑表单': 编辑表单,'用户': 请求.user}
    return render(请求, "myauth/edit_profile.html", 内容)

@login_required(login_url='myauth:登录')
def 修改密码(请求):
    if 请求.method == 'POST':
        改密表单 = PasswordChangeForm(data=请求.POST, user=请求.user)
        if 改密表单.is_valid():
            改密表单.save()
            return redirect("myauth:登录")
    else:
        改密表单 = PasswordChangeForm(user=请求.user)

    内容 = {'改密表单': 改密表单, '用户': 请求.user}
    return render(请求, "myauth/change_password.html", 内容)


def 主页(请求):
    return render(请求, 'myauth/home.html')

def 登录(请求):
    if 请求.method == 'POST':
        登录表单=自定义登录表单(data=请求.POST)
        if 登录表单.is_valid():
            用户 = authenticate(请求, username=登录表单.cleaned_data['username'], password=登录表单.cleaned_data['password'])
            login(请求, 用户)
            return redirect('myauth:主页')
    else:
        if 请求.user.is_authenticated:
            return redirect('myauth:主页')
        else:
            登录表单 = 自定义登录表单()

    内容 = {'登录表单': 登录表单, '用户': 请求.user}
    return render(请求, "myauth/login.html", 内容)
    
    
def 登出(请求):
    logout(请求)
    return redirect("myauth:主页")

def 注册(请求):
    if 请求.method == 'POST':
        注册表单 = 自定义注册表单(请求.POST)
        if 注册表单.is_valid():
            注册表单.save()
            用户 = authenticate(请求, username=注册表单.changed_data['username'],password=注册表单.changed_data['password1'])
            用户.email = 注册表单.cleaned_data['email']
            普通会员表(用户=用户,昵称=注册表单.cleaned_data['昵称'],生日=注册表单.cleaned_data['生日']).save()
            login(请求, 用户)
            return  redirect("myauth:主页")
        
    else:
        注册表单 = 自定义注册表单()
        
    内容 = {'注册表单': 注册表单}
    return render(请求, "myauth/register.html", 内容)