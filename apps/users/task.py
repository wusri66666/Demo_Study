from celery import task

from django.template import loader
from django.core.mail import send_mail

from MxOnline import settings
from users.models import EmailVerifyRecord


@task
def send_verify_mail(url,email,send_type='register'):
    code = url.rsplit('/',1)[-1]
    email_record = EmailVerifyRecord()
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = "Study_Demo在线教育网注册激活链接"
        email_body = url
        template = loader.get_template('email_template.html')
        template_str = template.render({'title': email_title, 'email_body': email_body})
        receivers = [email]
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(email_title, '', email_from, receivers, html_message=template_str)
    elif send_type == 'forget':
        email_title = "Study_Demo在线教育网密码重置链接"
        email_body = url
        template = loader.get_template('email_template.html')
        template_str = template.render({'title': email_title, 'email_body': email_body})
        receivers = [email]
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(email_title, '', email_from, receivers, html_message=template_str)
