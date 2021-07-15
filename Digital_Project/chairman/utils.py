from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def sendmail(subject,template,to,context):
    template_str = 'chairman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'patelpoojan6655@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailmember(subject,template,to,context): #otp for member forgot password
    template_str = 'user/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'patelpoojan6655@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def watchmanregistration(subject,template,to,context): #otp for member forgot password
    template_str = 'chairman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'patelpoojan6655@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailwatchman(subject,template,to,context): #otp for watchman forgot password
    template_str = 'watchman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'patelpoojan6655@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def sendmailtoMember(subject,template,to,context):
    template_str = 'chairman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'patelpoojan6655@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

