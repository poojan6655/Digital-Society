from django.db import models
from django.utils import timezone
import math
from datetime import datetime

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(default=459)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.email

class MemberCommonInformation(models.Model):
    # member_role=models.CharField(max_length=20)
    home_no=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    job_profession=models.CharField(max_length=20,blank=True)
    job_address=models.CharField(max_length=100,blank=True)
    vehicle_type=models.CharField(max_length=20,blank=True)
    vehicle_no=models.CharField(max_length=20,blank=True)
    blood_group=models.CharField(max_length=20,blank=True)
    family_member=models.CharField(max_length=20)
    contactno=models.CharField(max_length=13)
    home_pic=models.FileField(upload_to='img/',blank=True,default='home.jpg')

    def __str__(self):
        return self.home_no

class Chairman(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    m_id=models.ForeignKey(MemberCommonInformation,on_delete=models.CASCADE,default=False)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    # contactno=models.CharField(max_length=13)
    profile_pic=models.FileField(upload_to='img/',blank=True,default='default.jpg')

    def __str__(self):
        return self.fname

class MemberDetails(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    m_id=models.ForeignKey(MemberCommonInformation,on_delete=models.CASCADE,default=False)
    fname=models.CharField(max_length=20,default="Not Provided Yet")
    lname=models.CharField(max_length=20,default="Not Provided Yet")
    # contactno=models.CharField(max_length=13,default="Not Provided Yet")
    # Member_address=models.CharField(max_length=150,default="Not Provided Yet")
    profile_pic=models.FileField(upload_to='img/',blank=True,default='default.jpg')
     

    def __str__(self):
        return self.fname

class Watchman(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    # m_id=models.ForeignKey(MemberCommonInformation,on_delete=models.CASCADE,default=False)
    fname=models.CharField(max_length=20,default="Not Provided Yet")
    lname=models.CharField(max_length=20,default="Not Provided Yet")
    contactno=models.CharField(max_length=13)
    profile_pic=models.FileField(upload_to='img/',blank=True,default='default.jpg')
     

    def __str__(self):
        return self.fname

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class Maintenance(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default="",blank=True,null=True)
    member_id=models.ForeignKey(MemberDetails,on_delete=models.CASCADE,default="",blank=True,null=True)
    cid = models.ForeignKey(Chairman,on_delete=models.CASCADE,default="",blank=True,null=True)
    title = models.CharField(max_length=100,blank=True)
    amount = models.IntegerField(max_length=999,blank=True)
    due_date = models.DateTimeField(auto_now_add=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)
    status = models.CharField(max_length=20,default="Pending")

    def __str__(self):
        return self.title

class Balance(models.Model):
    title = models.CharField(max_length=100,blank=True)
    amount_have = models.IntegerField(max_length=999,blank=True)
    # remain_amount = models.IntegerField(max_length=999,default=10000,blank=True)
    date = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

class Expense(models.Model):
    balance_id=models.ForeignKey(Balance,on_delete=models.CASCADE,default="",blank=True,null=True)
    title = models.CharField(max_length=100,blank=True)
    Price = models.IntegerField(max_length=999,blank=True)
    date = models.DateTimeField(auto_now_add=True,blank=False)
    # updated_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

# class chat(models.Model):
#     sender = models.CharField(max_length=20)
#     recevier = models.CharField(max_length=20)
#     msg = models.CharField(max_length=200)
#     reply = models.CharField(max_length=200,default=False)
#     msg_send_at = models.DateTimeField(auto_now_add=True,blank=False)

#     def __str__(self):
#         return self.msg

class Images(models.Model):
    uploaded_by = models.CharField(max_length=30)
    imgName = models.CharField(max_length=20)
    pic = models.FileField(upload_to='images/',default='default.jpg')
    Uploaded_at = models.DateTimeField(auto_now_add=True,blank=False)

    def __str__(self):
        return self.imgName

class Videos(models.Model):
    uploaded_by = models.CharField(max_length=30)
    vidName = models.CharField(max_length=20)
    vid = models.FileField(upload_to='videos/',null=True, verbose_name="")
    Uploaded_at = models.DateTimeField(auto_now_add=True,blank=False)

    def __str__(self):
        return self.vidName

class Notice(models.Model):
    uploaded_by = models.CharField(max_length=20,default="not Found In Record")
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.title

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >=0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + " seconds ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minutes ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hours ago"

            else:
                return str(hours) + " hours ago"

        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " day ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " month ago"

        if diff.days >=365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " year ago"

class Post(models.Model):
    uploaded_by = models.CharField(max_length=20,default="not Found In Record")
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=200)
    post_uploaded_pic=models.FileField(upload_to='img/',blank=True,default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)
    # date = models.DateTimeField('Mon, 23 May 2016 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S %Z',default="not provided") 
    # date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    # profile_pic=models.FileField(upload_to='img/',blank=True,default='default.jpg')

    def __str__(self):
        return self.title


    def whenpublished(self):

        now = timezone.now()

        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >=0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + " seconds ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minutes ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hours ago"

            else:
                return str(hours) + " hours ago"

        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " day ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " month ago"

        if diff.days >=365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " year ago"





                