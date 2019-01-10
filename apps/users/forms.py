from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required':'用户名不能为空'})
    password = forms.CharField(error_messages={'required':'密码不能为空'})


class RegisterForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空'})
    password = forms.CharField(error_messages={'required': '密码不能为空'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgrtForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)