from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from users.forms import *
from users.models import *
from django.contrib.auth.hashers import make_password
from users.task import send_verify_mail
from users.utils.get_unique import get_unique_str


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email','')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'msg': '该用户已注册'})
            last_email = email.rsplit('@',1)[-1]
            password = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.username = email
            user_profile.is_active = 0
            user_profile.password = make_password(password)
            user_profile.save()
            url = 'http://'+request.get_host()+'/active/'+get_unique_str()
            send_verify_mail.delay(url,email,send_type='register')
            if last_email=='qq.com':
                url1 = 'https://mail.qq.com/'
            elif last_email=='163.com':
                url1 = "https://mail.163.com/"
            return render(request,'notice.html',{'email':url1})
        else:
            return render(request,'register.html',{'register_form':register_form})


def active(request,active_code):
    obj = EmailVerifyRecord.objects.filter(code=active_code).first()
    if obj:
        email = obj.email
        user = UserProfile.objects.get(email=email)
        user.is_active = 1
        user.save()
        return render(request,'login.html')
    else:
        return HttpResponse('链接已失效')
    return HttpResponse('没有该用户')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(username=name, password=pwd)
            if user:
                login(request, user)
                return render(request, 'index.html', {'user': user})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetPwdView(View):
    def get(self,request):
        forgetform = ForgrtForm()
        return render(request,'forgetpwd.html',{'forgetform':forgetform})

    def post(self,request):
        forget_form = ForgrtForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            url = 'http://'+request.get_host()+'/reset/'+get_unique_str()
            send_verify_mail.delay(url,email,send_type='forget')
            last_email = email.rsplit('@', 1)[-1]
            if last_email == 'qq.com':
                url1 = 'https://mail.qq.com/'
            elif last_email == '163.com':
                url1 = "https://mail.163.com/"
            return render(request, 'notice.html', {'email': url1})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self,request,active_code):
        obj = EmailVerifyRecord.objects.filter(code=active_code).first()
        if obj:
            email = obj.email
            return render(request,'password_reset.html',{'email':email})
        else:
            return HttpResponse('链接已失效')
        return HttpResponse('没有该用户')


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            render(request, 'password_reset.html', {'email': email,'modify_form':modify_form})

