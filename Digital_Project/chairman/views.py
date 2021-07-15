from django.shortcuts import render
from .models import *
# from django.core.mail import send_mail
from .utils import *
from random import *
from django.http import JsonResponse

from .paytm import generate_checksum,verify_checksum    #FOR PAYMENT
from django.conf import settings                        #FOR PAYMENT
from django.views.decorators.csrf import csrf_exempt    #FOR PAYMENT
# from notifications.signals import notify

# Create your views here.
def chairman_fun(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        if uid.role=="chairman":
            cid=Chairman.objects.get(user_id=uid)
            noticedata=Notice.objects.all()
            count = MemberDetails.objects.all().count()
            usercount = User.objects.all().count()

            maintenance_data=Maintenance.objects.filter(cid=cid)
            paymentid=Transaction.objects.all().order_by('made_on')
            balanceid=Balance.objects.get(title="Balance")
            maintenance_data_member=Maintenance.objects.all()
        
            context={
                    'uid':uid,
                    'cid':cid,
                    'noticedata':noticedata,
                    'count':count,
                    'usercount':usercount,
                    "maintenance_data":maintenance_data,
                    'paymentid':paymentid,
                    'maintenance_data_member':maintenance_data_member,
                    'balanceid':balanceid,
                    }
            return render(request,"chairman/index.html",{'context':context})
        elif uid.role=="user":
            cid=MemberDetails.objects.get(user_id=uid)
            # mid=MemberDetails.objects.all()
            count = MemberDetails.objects.all().count()
            usercount = User.objects.all().count()

            maintenance_data=Maintenance.objects.filter(member_id=cid)
            paymentid=Transaction.objects.filter(made_by=uid).order_by('made_on')
            balanceid=Balance.objects.get(title="Balance")
            maintenance_data_member=Maintenance.objects.all()

            noticedata=Notice.objects.all()
            context={
                    'uid':uid,
                    'cid':cid,
                    'noticedata':noticedata,
                    'count':count,
                    'usercount':usercount,
                    "maintenance_data":maintenance_data,
                    'paymentid':paymentid,
                    'maintenance_data_member':maintenance_data_member,
                    'balanceid':balanceid,
                    }
            return render(request,"user/index.html",{'context':context})
        elif uid.role=="watchman":
            cid=Watchman.objects.get(user_id=uid)
            count = MemberDetails.objects.all().count()
            usercount = User.objects.all().count()

            # maintenance_data=Maintenance.objects.filter(member_id=cid)
            # paymentid=Transaction.objects.filter(made_by=uid).order_by('made_on')
            expenseid=Expense.objects.all().order_by('-id')
            balanceid=Balance.objects.get(title="Balance")
            maintenance_data_member=Maintenance.objects.all()
            context={
                    'uid':uid,
                    'cid':cid,
                    'count':count,
                    'usercount':usercount,
                    # "maintenance_data":maintenance_data,
                    'expenseid':expenseid,
                    'maintenance_data_member':maintenance_data_member,
                    'balanceid':balanceid,
                    }
            return render(request,"watchman/index-watchman.html",{'context':context})
        else:
            e_msg="Please login Again...<3"
            return render(request,"chairman/login.html",{'e_msg':e_msg})
    else:
        return render(request,"chairman/login.html")


def registration_fun(request):
    if request.POST:
        role=request.POST['RoleFromHTML']
        if role=="watchman":
            email=request.POST['EmailFromHtml']
            password=request.POST['PasswordFromHtml']
            fname=request.POST['FnameFromHtml']
            lname=request.POST['LnameFromHtml']
            # mobileno=request.POST['MobileNoFromHtml']
            isactive="True"

            uid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
            uid.save()
            userdata=User.objects.all()


            wid=Watchman.objects.create(user_id=uid,fname=fname,lname=lname)
            wid.save()
            # wid=Watchman.objects.all()

            context={
                    'uid':uid,
                # 'cid':cid,
                    'userdata':userdata,
                    'wid':wid,
                    }
            s_msg="Added Successfully(wait for Chairman Approval)"
            watchmanregistration("Complete-Registration","Email-template-Watchman-registration",'ppoojan40@gmail.com',{'wid':wid})
            return render(request,"chairman/register.html",{'s_msg':s_msg,'context':context})
        else:
            email=request.POST['EmailFromHtml']
            password=request.POST['PasswordFromHtml']
            fname=request.POST['FnameFromHtml']
            lname=request.POST['LnameFromHtml']
            mobileno=request.POST['MobileNoFromHtml']
            isactive="True"

            uid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
            uid.save()

            mid=MemberDetails.objects.create(user_id=uid,fname=fname,lname=lname)
            mid.m_id.contactno=mobileno
            mid.m_id.save()
            mid.save()
            context={
                    'uid':uid,
                # 'cid':cid,
                    # 'userdata':userdata,
                    'mid':mid,
                    }
            # sendmail("Forgot - Password","Email-template-send-OTP",email,{'mid':mid})
            s_msg="Added Successfully(wait for Chairman Approval)"
            return render(request,"chairman/register.html",{'s_msg':s_msg,'context':context})
    else:
        return render(request,"chairman/register.html")

# def registration_evalute_fun(request):
#         role=request.POST['RoleFromHTML']
#         if role=="watchman":
#             email=request.POST['EmailFromHtml']
#             password=request.POST['PasswordFromHtml']
#             fname=request.POST['FnameFromHtml']
#             lname=request.POST['LnameFromHtml']
#             # mobileno=request.POST['MobileNoFromHtml']
#             isactive="True"

#             uid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
#             uid.save()
#             userdata=User.objects.all()


#             wid=Watchman.objects.create(user_id=uid,fname=fname,lname=lname)
#             wid.save()
#             wid=Watchman.objects.all()

#             context={
#                     'uid':uid,
#                 # 'cid':cid,
#                     'userdata':userdata,
#                     'wid':wid,
#                     }
#             s_msg="Added Successfully(wait for Chairman Approval)"
#             sendmail("Forgot - Password","Email-template-send-OTP",'ppoojan40@gmail.com',{'wid':wid})
#             return render(request,"chairman/login.html",{'s_msg':s_msg,'context':context})
#         else:
#             email=request.POST['EmailFromHtml']
#             password=request.POST['PasswordFromHtml']
#             fname=request.POST['FnameFromHtml']
#             lname=request.POST['LnameFromHtml']
#             mobileno=request.POST['MobileNoFromHtml']
#             isactive="True"

#             uid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
#             uid.save()

#             mid=MemberDetails.objects.create(user_id=uid,fname=fname,lname=lname,contactno=mobileno)
#             mid.save()
#             context={
#                     'uid':uid,
#                 # 'cid':cid,
#                     # 'userdata':userdata,
#                     'mid':mid,
#                     }
#             sendmail("Forgot - Password","Email-template-send-OTP",email,{'mid':mid})
#             s_msg="Added Successfully(wait for Chairman Approval)"
#             return render(request,"chairman/login.html",{'s_msg':s_msg,'context':context})
#     else:
#         return render(request,"chairman/login.html")

def login_fun(request):
    if request.POST:
        u_email=request.POST['EmailFromHtml']
        u_password=request.POST['PasswordFromHtml']

        uid=User.objects.get(email=u_email)
        if uid.password==u_password:
            if uid.role=="chairman":
                request.session['c_email']=uid.email

                cid=Chairman.objects.get(user_id=uid)

                count = MemberDetails.objects.all().count()
                usercount = User.objects.all().count()
                maintenance_data=Maintenance.objects.filter(cid=cid)
                paymentid=Transaction.objects.all().order_by('made_on')
                balanceid=Balance.objects.get(title="Balance")
                maintenance_data_member=Maintenance.objects.all()
                context={
                        'uid':uid,
                        'cid':cid,
                        # 'noticedata':noticedata,
                        'count':count,
                        'usercount':usercount,
                        "maintenance_data":maintenance_data,
                        'paymentid':paymentid,
                        'maintenance_data_member':maintenance_data_member,
                        'balanceid':balanceid,
                        }
                # send_mail("welcome","hello email","patelpoojan6655@gmail.com",u_email)

                return render(request,"chairman/index.html",{'context':context})
            elif uid.role=="user":
                request.session['c_email']=uid.email
                cid=MemberDetails.objects.get(user_id=uid)
                count = MemberDetails.objects.all().count()
                usercount = User.objects.all().count()

                maintenance_data=Maintenance.objects.filter(member_id=cid)
                paymentid=Transaction.objects.filter(made_by=uid).order_by('made_on')
                balanceid=Balance.objects.get(title="Balance")
                maintenance_data_member=Maintenance.objects.all()

                noticedata=Notice.objects.all()
                context={
                        'uid':uid,
                        'cid':cid,
                        'noticedata':noticedata,
                        'count':count,
                        'usercount':usercount,
                        "maintenance_data":maintenance_data,
                        'paymentid':paymentid,
                        'maintenance_data_member':maintenance_data_member,
                        'balanceid':balanceid,
                        }
                return render(request,"user/index.html",{'context':context})
            elif uid.role=="watchman":
                if uid.is_verified==True:
                    request.session['c_email']=uid.email
                    cid=Watchman.objects.get(user_id=uid)
                    count = MemberDetails.objects.all().count()
                    usercount = User.objects.all().count()

                    # maintenance_data=Maintenance.objects.filter(member_id=cid)
                    # paymentid=Transaction.objects.filter(made_by=uid).order_by('made_on')
                    expenseid=Expense.objects.all().order_by('-id')
                    balanceid=Balance.objects.get(title="Balance")
                    maintenance_data_member=Maintenance.objects.all()
                    context={
                            'uid':uid,
                            'cid':cid,
                            'count':count,
                            'usercount':usercount,
                            # "maintenance_data":maintenance_data,
                            'expenseid':expenseid,
                            'maintenance_data_member':maintenance_data_member,
                            'balanceid':balanceid,
                            }
                    return render(request,"watchman/index-watchman.html",{'context':context})
                else:
                    e_msg="You are not Varified by chairman"
                    return render(request,"chairman/login.html",{'e_msg':e_msg})
            else:
                e_msg="User is Not Found"
                return render(request,"chairman/login.html",{'e_msg':e_msg})
        else:
            e_msg="invalid password"
            return render(request,"chairman/login.html",{'e_msg':e_msg})
    else:
        return render(request,"chairman/login.html")

# def login_evalute(request):
#     try:
#         u_email=request.POST['EmailFromHtml']
#         u_password=request.POST['PasswordFromHtml']

#         uid=User.objects.get(email=u_email)
#         if uid.password==u_password:
#             if uid.role=="chairman":
#                 print("---------------hello")
#                 request.session['c_email']=uid.email

#                 cid=Chairman.objects.get(user_id=uid)
#                 context={
#                     'uid':uid,
#                     'cid':cid,
#                     }

#                 # send_mail("welcome","hello email","patelpoojan6655@gmail.com",u_email)

#                 return render(request,"chairman/index.html",{'context':context})
#             elif uid.role=="user":
#                 request.session['c_email']=uid.email
#                 mid=MemberDetails.objects.get(user_id=uid)
#                 context={
#                     'uid':uid,
#                     'mid':mid,
#                     }
#                 return render(request,"user/index.html",{'context':context})
#             else:
#                 e_msg="User is Not Found"
#                 return render(request,"chairman/login.html",{'e_msg':e_msg})
#         else:
#             e_msg="invalid password"
#             return render(request,"chairman/login.html",{'e_msg':e_msg})
#     except:
#         e_msg="email does not exist"
#         return render(request,"chairman/login.html",{'e_msg':e_msg})





def logout_fun(request):
    if "c_email" in request.session:
        del request.session['c_email']
        return render(request,"chairman/login.html")
    else:
        return render(request,"chairman/login.html")

def forgot_password_fun(request):
    return render(request,"chairman/forgot-password.html")

def send_OTP_fun(request):
    # try:
    u_email=request.POST['EmailFromHtml']
    generateOTP=randint(1111,9999)
    uid=User.objects.get(email=u_email)
    # if uid:
            

    if uid.role=="chairman":
        uid.otp=generateOTP
        uid.save() #update
        cid=Chairman.objects.get(user_id=uid)
        sendmail("Forgot - Password","Email-template-send-OTP",u_email,{'otp':generateOTP,'cid':cid})
        return render(request,"chairman/OTP-Receive.html",{'u_email':u_email})
    elif uid.role=="user":
        uid.otp=generateOTP
        uid.save() #update
        mid=MemberDetails.objects.get(user_id=uid)
        sendmailmember("Forgot - Password","Member-Email-template-send-OTP",u_email,{'otp':generateOTP,'mid':mid})
        return render(request,"chairman/OTP-Receive.html",{'u_email':u_email})
    elif uid.role=="watchman":
        uid.otp=generateOTP
        uid.save() #update
        wid=Watchman.objects.get(user_id=uid)
        sendmailwatchman("Forgot - Password","Watchman-Email-template-send-OTP",u_email,{'otp':generateOTP,'wid':wid})
        return render(request,"chairman/OTP-Receive.html",{'u_email':u_email})
    else:
        e_msg="invalid Email"
        return render(request,"chairman/forgot-password.html",{'e_msg':e_msg})
    # except:
    #     e_msg="Email does not exist"
    #     return render(request,"chairman/forgot-password.html",{'e_msg':e_msg})


def OTP_Receive_fun(request):
    u_email=request.POST['EmailFromHtml']
    otp=request.POST['OTPFromHtml']
    uid=User.objects.get(email=u_email)
    if uid:
        if str(uid.otp)==otp:
            return render(request,"chairman/Reset-Password.html",{'u_email':u_email})
        else:
            e_msg="invalid OTP"
            return render(request,"chairman/OTP-Receive.html",{'e_msg':e_msg})
    else:
        e_msg="invalid OTP"
        return render(request,"chairman/forgot-password.html")

def Reset_Password_fun(request):
    u_email=request.POST['EmailFromHtml']
    newpassword=request.POST['PasswordFromHtml']
    repassword=request.POST['Re-PasswordFromHtml']
    uid=User.objects.get(email=u_email)
    if uid:
        if newpassword==repassword:
            uid.password=newpassword
            uid.save() # NEW Password save to database
            s_msg="Succcessfully Reset Password"
            return render(request,"chairman/login.html",{'s_msg':s_msg})
        else:
            e_msg="password not match"
            return render(request,"chairman/Reset-password.html",{'e_msg':e_msg})
    else:
        e_msg="invalid USER"
        return render(request,"chairman/forgot-password.html")

# def chairman_chat_fun(request,pk):
#     uid=User.objects.get(email=request.session['c_email'])
#     if uid.role=="chairman":
#         cid=Chairman.objects.get(user_id=uid)
#         mid=MemberDetails.objects.all()
#         memberdata=MemberDetails.objects.get(id=pk)
#         context={
#             'uid':uid,
#             'cid':cid,
#             'mid':mid,
#             'memberdata':memberdata,
#                 }
#         return render(request,"chairman/chariman-chat.html",{'context':context})
#     elif uid.role=="user":
#         cid=MemberDetails.objects.get(user_id=uid)
#         mid=MemberDetails.objects.all()
#         memberdata=MemberDetails.objects.get(id=pk)
#         context={
#                 'uid':uid,
#                 'cid':cid,
#                 'mid':mid,
#                 'memberdata':memberdata,
#                 }
#         return render(request,"chairman/chariman-chat.html",{'context':context})
#     else:
#         pass

# def send_msg_page_fun(request):
#     uid=User.objects.get(email=request.session['c_email'])
#     if uid.role=="chairman":
#         cid=Chairman.objects.get(user_id=uid)
#         sender = cid.user_id.email
#         recevier=request.POST['userid']
#         message=request.POST['typemsgFromHTML']
#         chatid = chat.objects.create(sender=sender,recevier=recevier,msg=message)
#         # notify.send(sender, recipient=recevier, verb='Message', description=request.POST.get('message'))
#         userdata=User.objects.get(email=recevier)
#         memberdata=MemberDetails.objects.get(user_id=userdata)
#         print("fffffffffffffffffffffffffffffffffff",recevier)
#         context={
#                 'chatid':chatid,
#                 'uid':uid,
#                 'cid':cid,
#                 'memberdata':memberdata,
#                 # 'mid':mid,
#                 }
#         return render(request,"chairman/chariman-chat.html",{'context':context})

def add_notice_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        context={
            'uid':uid,
            'cid':cid,
                    }
        return render(request,"chairman/add-notice.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        context={
                'uid':uid,
                'cid':cid,
                }
        return render(request,"user/add-notice.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        context={
                'uid':uid,
                'cid':cid,
                }
        return render(request,"watchman/add-notice.html",{'context':context})
    # else:
    #     return render(request,"chairman/index.html")

# def notice_added_fun(request):
#     title=request.POST['NoticeFromHtml']
#     descript=request.POST['DescriptionFromHtml']
#     nid=Notice.objects.create(title=title,description=descript) #creating notice
#     nid.save()
#     uid=User.objects.get(email=request.session['c_email'])
#     if uid.role=="chairman":
#         cid=Chairman.objects.get(user_id=uid)
#         noticedata=Notice.objects.all()
#         context={
#                 'uid':uid,
#                 'cid':cid,
#                 'noticedata':noticedata,
#                 }
#         return render(request,"chairman/view-notice.html",{'context':context})
#     elif uid.role=="user":
#         mid=MemberDetails.objects.get(user_id=uid)
#         noticedata=Notice.objects.all()
#         context={
#                 'uid':uid,
#                 'mid':mid,
#                 'noticedata':noticedata,
#                 }
#         return render(request,"chairman/view-notice.html",{'context':context})

    
def view_notice_fun(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        if request.POST:
            # uid=User.objects.get(email=request.session['c_email'])
            if uid.role=="chairman":
                cid=Chairman.objects.get(user_id=uid)
                title=request.POST['NoticeFromHtml']
                descript=request.POST['DescriptionFromHtml']
                noticegivenby=cid.fname
                nid=Notice.objects.create(title=title,description=descript,uploaded_by=noticegivenby) #creating notice
                nid.save()
                noticedata=Notice.objects.all().order_by('-id')
                context={
                        'uid':uid,
                        'cid':cid,
                        'noticedata':noticedata,
                        }
                return render(request,"chairman/view-notice.html",{'context':context})
            elif uid.role=="user":
                cid=MemberDetails.objects.get(user_id=uid)
                title=request.POST['NoticeFromHtml']
                descript=request.POST['DescriptionFromHtml']
                noticegivenby=cid.fname
                nid=Notice.objects.create(title=title,description=descript,uploaded_by=noticegivenby) #creating notice
                nid.save()
                noticedata=Notice.objects.all().order_by('-id')
                context={
                        'uid':uid,
                        'cid':cid,
                        'noticedata':noticedata,
                        }
                return render(request,"user/view-notice.html",{'context':context})
            else:
                cid=Watchman.objects.get(user_id=uid)
                title=request.POST['NoticeFromHtml']
                descript=request.POST['DescriptionFromHtml']
                noticegivenby=cid.fname
                nid=Notice.objects.create(title=title,description=descript,uploaded_by=noticegivenby) #creating notice
                nid.save()
                noticedata=Notice.objects.all().order_by('-id')
                context={
                        'uid':uid,
                        'cid':cid,
                        'noticedata':noticedata,
                        }
                return render(request,"watchman/view-notice.html",{'context':context})
        else:
            # uid=User.objects.get(email=request.session['c_email'])
            if uid.role=="chairman":
                cid=Chairman.objects.get(user_id=uid)
                mid=MemberDetails.objects.all()
                noticedata=Notice.objects.all().order_by('-id')
                context={
                    'uid':uid,
                    'cid':cid,
                    'noticedata':noticedata,
                    'mid':mid,
                    }
                return render(request,"chairman/view-notice.html",{'context':context})
            elif uid.role=="user":
                cid=MemberDetails.objects.get(user_id=uid)
                # cid=Chairman.objects.all()
                noticedata=Notice.objects.all().order_by('-id')
                context={
                    'uid':uid,
                    'cid':cid,
                    'noticedata':noticedata,
                    # 'mid':mid,
                    }
                return render(request,"user/view-notice.html",{'context':context})
            else:
                cid=Watchman.objects.get(user_id=uid)
                noticedata=Notice.objects.all().order_by('-id')
                context={
                    'uid':uid,
                    'cid':cid,
                    'noticedata':noticedata,
                    # 'mid':mid,
                    }
                return render(request,"watchman/view-notice.html",{'context':context})

def delete_notice_fun(request,pk):    
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        noticedata=Notice.objects.get(id=pk)
        noticedata.delete()
        noticedata=Notice.objects.all().order_by('-id')
            # pid=Post.objects.get(home_no=houseno)
        context={
                'uid':uid,
                'cid':cid,
                'noticedata':noticedata,
                }
        return render(request,"chairman/view-notice.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        # pid=Post.objects.all()
        noticedata=Notice.objects.get(id=pk)
        noticedata.delete()
        noticedata=Notice.objects.all().order_by('-id')
        context={
                'uid':uid,
                'cid':cid,
                'noticedata':noticedata,
                # 'pid':pid,
                }
        return render(request,"user/view-notice.html",{'context':context})

def add_post_fun(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        if request.POST:
            posttitle=request.POST['PostTitleFromHtml']
            postdescript=request.POST['PostDescriptionFromHtml']
            pid=Post.objects.create(title=posttitle,description=postdescript) #creating pid
    
            if "PostPhotoFromHtml" in request.FILES:
                profilepicture=request.FILES['PostPhotoFromHtml']
                pid.post_uploaded_pic=profilepicture
                pid.save()
            else:
                pass

            

            if uid.role=="chairman":
                cid=Chairman.objects.get(user_id=uid)
                pid.uploaded_by=cid.fname
                pid.save()
                pid=Post.objects.all().order_by('-id')
                context={
                    'uid':uid,
                    'cid':cid,
                    'pid':pid,
                    # 'postdata':postdata,
                    }
                return render(request,"chairman/view-post.html",{'context':context})
            elif uid.role=="user":
                cid=MemberDetails.objects.get(user_id=uid)
                pid.uploaded_by=cid.fname
                pid.save()
                pid=Post.objects.all().order_by('-id')
                context={
                    'uid':uid,
                    'cid':cid,
                    'pid':pid,
                    # 'postdata':postdata,
                    }
                return render(request,"user/view-post.html",{'context':context})
            else:
                pass
        else:
            if uid.role=="chairman":
                cid=Chairman.objects.get(user_id=uid)
                # mid=MemberDetails.objects.all()
                context={
                        'uid':uid,
                        'cid':cid,
                        # 'mid':mid,
                        }
                return render(request,"chairman/add-post.html",{'context':context})
            elif uid.role=="user":
                cid=MemberDetails.objects.get(user_id=uid)
                context={
                        'uid':uid,
                        'cid':cid,
                        }
                return render(request,"user/add-post.html",{'context':context})
            else:
                pass
    else:
        return render(request,"chairman/index.html")

def view_post_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        pid=Post.objects.all().order_by('-id')
        context={
                'uid':uid,
                'cid':cid,
                'pid':pid,
                }
        return render(request,"chairman/view-post.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        pid=Post.objects.all().order_by('-id')
        context={
                'uid':uid,
                'cid':cid,
                'pid':pid,
                }
        return render(request,"user/view-post.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        pid=Post.objects.all().order_by('-id')
        context={
                'uid':uid,
                'cid':cid,
                'pid':pid,
                }
        return render(request,"watchman/view-events.html",{'context':context})

def delete_post_fun(request,pk):    
    uid=User.objects.get(email=request.session['c_email'])
    pid=Post.objects.get(id=pk)
    pid.delete()
    pid=Post.objects.all().order_by('-id')
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
            # pid=Post.objects.get(home_no=houseno)
        context={
                'uid':uid,
                'cid':cid,
                'pid':pid,
                }
        return render(request,"chairman/view-post.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        # pid=Post.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                'pid':pid,
                }
        return render(request,"user/view-post.html",{'context':context})

def calendar_fun(request):
    if "c_email" in request.session:
        uid=User.objects.get(email=request.session['c_email'])
        # cid=Chairman.objects.get(user_id=uid)
        # eventdata=Post.objects.all()
        # context={
        #         'uid':uid,
        #         'cid':cid,
        #         'eventdata':eventdata,
        #         }
        # return render(request,"chairman/calendar.html",{'context':context})    
        if uid.role=="chairman":
            cid=Chairman.objects.get(user_id=uid)
            eventdata=Post.objects.all().order_by('-id')
            context={
                    'uid':uid,
                    'cid':cid,
                    'eventdata':eventdata,
                    }
            return render(request,"chairman/calendar.html",{'context':context})
        elif uid.role=="user":
            cid=MemberDetails.objects.get(user_id=uid)
            eventdata=Post.objects.all().order_by('-id')
            context={
                    'uid':uid,
                    'cid':cid,
                    'eventdata':eventdata,
                    }
            return render(request,"user/calendar.html",{'context':context})
        else:
            cid=Watchman.objects.get(user_id=uid)
            eventdata=Post.objects.all().order_by('-id')
            context={
                    'uid':uid,
                    'cid':cid,
                    'eventdata':eventdata,
                    }
            return render(request,"watchman/calendar.html",{'context':context})


def add_member_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    # pid=Post.objects.get(home_no=houseno)
    # postdata=Post.objects.all()
    context={
            'uid':uid,
            'cid':cid,
            # 'postdata':postdata,
            }
    return render(request,"chairman/add-members.html",{'context':context})

def add_family_member_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    if request.POST:
        email=request.POST['EmailFromHTML']
        password=request.POST['PasswordFromHTML']
        # isactive=request.POST['IsActiveFromHTML']
        # isvarified=request.POST['IsActiveFromHTML']
        role=request.POST['RoleFromHTML']

        firstname=request.POST['FirstNameFromHTML']
        lastname=request.POST['LastNameFromHTML']

        houseNo=request.POST['HouseNoFromHTML']
        # houseNo=request.POST.get('HouseNoFromHTML', False)
        phoneNO=request.POST['PhoneFromHTML']
        bloddgrup=request.POST['BloodFromHTML']
        jobtype=request.POST['JobFromHTML']
        jobaddress=request.POST['JobAddressFromHTML']



        mcid=MemberCommonInformation.objects.get(home_no=houseNo)

        userid=User.objects.create(email=email,password=password,is_active="True",role=role,otp="1234",created_at="not provided",updated_at="not provided")
        userid.save()
        userdata=User.objects.all()

        


        mpid=MemberDetails.objects.create(m_id=mcid,user_id=userid,fname=firstname,lname=lastname)
        mpid.save()
        mid=MemberDetails.objects.all()

        mcid=MemberCommonInformation.objects.all()
        
        context={
                'uid':uid,
                'cid':cid,
                # 'postdata':postdata,
                'mcid':mcid,
                # 'userdata':userdata,
                'mid':mid,
                'mcid':mcid,
                # 'memberdata':memberdata,
                # 'memberpersonaldata':memberpersonaldata,
                }
        return render(request,"chairman/member-list.html",{'context':context})
    else:
        mcid = MemberCommonInformation.objects.all()
        # pid=Post.objects.get(home_no=houseno)
        # postdata=Post.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                # 'postdata':postdata,
                'mcid':mcid,
                }
        return render(request,"chairman/add-family-member.html",{'context':context})



def member_added_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    # mid=MemberDetails.objects.get(user_id=uid)

    email=request.POST['EmailFromHTML']
    password=request.POST['PasswordFromHTML']
    isactive=request.POST['IsActiveFromHTML']
    # isvarified=request.POST['IsActiveFromHTML']
    role=request.POST['RoleFromHTML']

    firstname=request.POST['FirstNameFromHTML']
    lastname=request.POST['LastNameFromHTML']

    houseNo=request.POST['HouseNoFromHTML']
    Houseaddress=request.POST['HouseAddressFromHTML']
    jobtype=request.POST['JobFromHTML']
    jobaddress=request.POST['JobAddressFromHTML']
    VehicleNo=request.POST['VehicleNoFromHTML']
    phoneNO=request.POST['PhoneFromHTML']
    bloddgrup=request.POST['BloodFromHTML']
    FamilyMembers=request.POST['FamilyMemberNoFromHTML']

    # try:
    #     memdata=MemberCommonInformation.objects.get(home_no=houseNo)
    # # house=memdata.home_no
    #     userid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
    #     userid.save()
    #     userdata=User.objects.all()
        
    #     mid=MemberCommonInformation.objects.get(home_no=houseNo)
    #     # mid.address=Houseaddress
    #     # mid.job_address=jobaddress
    #     # mid.job_profession=jobtype
    #     # mid.vehicle_no=VehicleNo
    #     # mid.contactno=phoneNO
    #     # mid.create(address=Houseaddress,job_address=jobaddress,job_profession=jobtype,vehicle_no=VehicleNo,contactno=phoneNO,blood_group=bloddgrup,family_member=FamilyMembers)
    #     mid=MemberCommonInformation.objects.create(address=Houseaddress,job_address=jobaddress,job_profession=jobtype,vehicle_no=VehicleNo,contactno=phoneNO,blood_group=bloddgrup,family_member=FamilyMembers)
    #     mid.save()
    #     memberdata=MemberCommonInformation.objects.all()
        
    #     mpid=MemberDetails.objects.create(m_id=mid,user_id=userid,fname=firstname,lname=lastname)
    #     mpid.save()
    #     memberpersonaldata=MemberDetails.objects.all()
        
    #     uid.save()
    #     userdata=User.objects.all()
    #     mid.save()
    #     memberdata=MemberCommonInformation.objects.all()
    #     mpid.save()
    #     memberpersonaldata=MemberDetails.objects.all()
    #     context={
    #             'uid':uid,
    #             'cid':cid,
    #             'userdata':userdata,
    #             'memberdata':memberdata,
    #             'memberpersonaldata':memberpersonaldata,
    #             # 'mid':mid,
    #             }
    #     sendmailtoMember("Successful-Register","Email-send-to-MemberOfSoc",mpid.user_id.email,{'mpid':mpid,'userdata':userdata,})
    #     s_msg="Member Added Successfully"
    #     return render(request,"chairman/member-list.html",{'s_msg':s_msg,'context':context})

    # except:
    userid=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
    userid.save()
    userdata=User.objects.all()
        
        # mid=MemberCommonInformation.objects.get(home_no=houseNo)
        
    mid=MemberCommonInformation.objects.create(home_no=houseNo,address=Houseaddress,job_address=jobaddress,job_profession=jobtype,vehicle_no=VehicleNo,contactno=phoneNO,blood_group=bloddgrup,family_member=FamilyMembers)
    mid.save()
    memberdata=MemberCommonInformation.objects.all()
        
    mpid=MemberDetails.objects.create(m_id=mid,user_id=userid,fname=firstname,lname=lastname)
    mpid.save()
    memberpersonaldata=MemberDetails.objects.all()
        
    uid.save()
    userdata=User.objects.all()
    mid.save()
    memberdata=MemberCommonInformation.objects.all()
    mpid.save()
    memberpersonaldata=MemberDetails.objects.all()
    mcid=MemberCommonInformation.objects.all()
    mid=MemberDetails.objects.all()
    context={
            'uid':uid,
            'cid':cid,
            'userdata':userdata,
            'mid':mid,
            'mcid':mcid,
                # 'mid':mid,
            }
    sendmailtoMember("Successful-Register","Email-send-to-MemberOfSoc",mpid.user_id.email,{'mpid':mpid,'userdata':userdata,})
    s_msg="Member Added Successfully"
    return render(request,"chairman/member-list.html",{'s_msg':s_msg,'context':context})

def member_list_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    # cid=Chairman.objects.get(user_id=uid)
    
    # mid=MemberDetails.objects.all()
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"chairman/member-list.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)     #Member id save on cid so will display where cid passed 
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        # mid=Che.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"user/member-list.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"watchman/member-list.html",{'context':context})

def watchman_list_approval_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        wid=Watchman.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                'wid':wid,
                # 'mcid':mcid,
                }
        return render(request,"chairman/watchman-list-approval.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        wid=Watchman.objects.all()
        # user=User.objects.filter(role="watchman")
        # user=User.objects.filter(is_verified=True)
        # wid=Watchman.objects.all(user_id=user)
        context={
                'uid':uid,
                'cid':cid,
                'wid':wid,
                # 'mcid':mcid,
                }
        return render(request,"user/watchman.html",{'context':context})


def watchman_approval_fun(request,pk):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)

    wid=Watchman.objects.get(id=pk)

    # email=request.POST['emailfromhtml']
    # userid=User.objects.get(email=email)
    approval="True"
    # wid=Watchman.objects.get(user_id=userid)
    wid.user_id.is_verified=approval
    wid.user_id.save()
    wid.save()
    wid=Watchman.objects.all()

    context={
            'uid':uid,
            'cid':cid,
            'wid':wid,
            # 'mcid':mcid,
            }
    return render(request,"chairman/watchman-list-approval.html",{'context':context})

def my_society_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"chairman/MySociety.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)     #Member id save on cid so will display where cid passed 
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        # mid=Che.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"user/MySociety.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.all()
        mid=MemberDetails.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        return render(request,"watchman/MySociety.html",{'context':context})

def family_member_list_fun(request,pk):
    uid=User.objects.get(email=request.session['c_email'])
    # cid=Chairman.objects.get(user_id=uid)
    # mcid=MemberCommonInformation.objects.get(id=pk)
    # # if MemberDetails.m_id==mcid:
    # # mid=MemberDetails.objects.all()

    # mid=MemberDetails.objects.filter(m_id=mcid)
    # context={
    #         'uid':uid,
    #         'cid':cid,
    #         'mcid':mcid,
    #         'mid':mid,
    #         }
    # return render(request,"chairman/Family-Member-list.html",{'context':context})
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.get(id=pk)
        mid=MemberDetails.objects.filter(m_id=mcid)
        if mid:
            context={
                'uid':uid,
                'cid':cid,
                'mcid':mcid,
                'mid':mid,
                }
            return render(request,"chairman/Family-Member-list.html",{'context':context})
        else:
            mid=Chairman.objects.filter(m_id=mcid)
            context={
                'uid':uid,
                'cid':cid,
                'mcid':mcid,
                'mid':mid,
                }
            return render(request,"chairman/Family-Member-list.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.get(id=pk)
        mid=MemberDetails.objects.filter(m_id=mcid)
        # uid=User.objects.get(email=mcid.email)
        if mid:
            # mid=MemberDetails.objects.filter(m_id=mcid)
            context={
            'uid':uid,
            'cid':cid,
            'mcid':mcid,
            'mid':mid,
            }
            return render(request,"user/Family-Member-list.html",{'context':context})
        else:
            mid=Chairman.objects.filter(m_id=mcid)
            context={
            'uid':uid,
            'cid':cid,
            'mcid':mcid,
            'mid':mid,
            }
            return render(request,"user/Family-Member-list.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        mcid=MemberCommonInformation.objects.get(id=pk)
        mid=MemberDetails.objects.filter(m_id=mcid)
        if mid:
            context={
                'uid':uid,
                'cid':cid,
                'mcid':mcid,
                'mid':mid,
                }
            return render(request,"watchman/family-member-list.html",{'context':context})
        else:
            mid=Chairman.objects.filter(m_id=mcid)            
            context={
                'uid':uid,
                'cid':cid,
                'mcid':mcid,
                'mid':mid,
                }
            return render(request,"watchman/family-member-list.html",{'context':context})

def my_profile_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    # noticedata=Notice.objects.all()
    context={
            'uid':uid,
            'cid':cid,
            # 'noticedata':noticedata,
            }
    return render(request,"chairman/my-profile-page.html",{'context':context})

def profile_update_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    newpassword=request.POST['NewPasswordFromHtml']
    confirmpassword=request.POST['ConfirmNewPasswordFromHtml']

    if newpassword==confirmpassword:
        fname=request.POST['FNameFromHtml']
        lname=request.POST['LNameFromHtml']
        JobProfession=request.POST['JobFromHtml']
        Contact=request.POST['ContactNumberFromHtml']
        houseno=request.POST['HouseNumberFromHtml']

        uid.password=newpassword
        cid.fname=fname
        cid.lname=lname
        mid=MemberCommonInformation.objects.get(home_no=houseno)
        mid.job_profession=JobProfession

        if "ProfilePicFromHtml" in request.FILES:
            profilepicture=request.FILES['ProfilePicFromHtml']
            cid.profile_pic=profilepicture
            cid.save()

        mid.contactno=Contact
        uid.save()
        cid.save()
        mid.save()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            }
        s_msg="Successfully Upadated"
        return render(request,"chairman/my-profile-page.html",{'s_msg':s_msg,'context':context})
    else:
        e_msg="Password Not Match"
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"chairman/my-profile-page.html",{'e_msg':e_msg,'context':context})

def All_images_collection_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":   
        cid=Chairman.objects.get(user_id=uid) 
        if request.POST:
            imagename=request.POST['imgnameFromhtml']
            imgget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            imgid=Images.objects.create(imgName=imagename ,pic=imgget ,uploaded_by=uploadBy)
            imgid=Images.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'imgid':imgid,
            }
            return render(request,"chairman/All-images.html",{'context':context})
        else:
            imgid=Images.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'imgid':imgid,
            }
            return render(request,"chairman/All-images.html",{'context':context})
    elif uid.role=="user":  
        cid=MemberDetails.objects.get(user_id=uid)  
        if request.POST:
            imagename=request.POST['imgnameFromhtml']
            imgget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            imgid=Images.objects.create(imgName=imagename ,pic=imgget ,uploaded_by=uploadBy)
            imgid=Images.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'imgid':imgid,
            }
            return render(request,"user/All-images.html",{'context':context})
        else:
            imgid=Images.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'imgid':imgid,
            }
            return render(request,"user/All-images.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid) 
        if request.POST:
            imagename=request.POST['imgnameFromhtml']
            imgget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            imgid=Images.objects.create(imgName=imagename ,pic=imgget ,uploaded_by=uploadBy)
            imgid=Images.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'imgid':imgid,
            }
            return render(request,"watchman/All-images.html",{'context':context})
        else:
            imgid=Images.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'imgid':imgid,
            }
            return render(request,"watchman/All-images.html",{'context':context})

def All_videos_collection_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":   
        cid=Chairman.objects.get(user_id=uid)
        if request.POST:
            videoname=request.POST['imgnameFromhtml']
            vidget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            vidid=Videos.objects.create(vidName=videoname ,vid=vidget ,uploaded_by=uploadBy)
            vidid=Videos.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'vidid':vidid,
            }
            return render(request,"chairman/All-Videos.html",{'context':context})
        else:
            vidid=Videos.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'vidid':vidid,
            }
            return render(request,"chairman/All-Videos.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        if request.POST:
            videoname=request.POST['imgnameFromhtml']
            vidget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            vidid=Videos.objects.create(vidName=videoname ,vid=vidget ,uploaded_by=uploadBy)
            vidid=Videos.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'vidid':vidid,
            }
            return render(request,"user/All-Videos.html",{'context':context})
        else:
            vidid=Videos.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'vidid':vidid,
            }
            return render(request,"user/All-Videos.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        if request.POST:
            videoname=request.POST['imgnameFromhtml']
            vidget=request.FILES['imgFromhtml']
            uploadBy=cid.fname
            vidid=Videos.objects.create(vidName=videoname ,vid=vidget ,uploaded_by=uploadBy)
            vidid=Videos.objects.all().order_by('-id')
            context={
            'uid':uid,
            'cid':cid,
            'vidid':vidid,
            }
            return render(request,"watchman/All-Videos.html",{'context':context})
        else:
            vidid=Videos.objects.all().order_by('-id')
            context={
                'uid':uid,
                'cid':cid,
                'vidid':vidid,
            }
            return render(request,"watchman/All-Videos.html",{'context':context})

#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----
# ----------------------member fun (profile show in chairman.index-page.member-list.onclickOf.ViewProfile)-------------------------------------------------------------

def chairman_member_profile_fun(request,pk):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        mid=MemberDetails.objects.get(id=pk)
        # noticedata=Notice.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                'mid':mid,
                # 'noticedata':noticedata,
                }
        return render(request,"chairman/m-profile.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        mid=MemberDetails.objects.get(id=pk)
        # noticedata=Notice.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                'mid':mid,
                # 'noticedata':noticedata,
                }
        return render(request,"user/m-profile.html",{'context':context})
    else:
        cid=Watchman.objects.get(user_id=uid)
        mid=MemberDetails.objects.get(id=pk)
        # noticedata=Notice.objects.all()
        context={
                'uid':uid,
                'cid':cid,
                'mid':mid,
                # 'noticedata':noticedata,
                }
        return render(request,"watchman/m-profile.html",{'context':context})


def chairman_member_profile_update_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    # mid=MemberDetails.objects.get(id=pk)

    houseno=request.POST['HouseNumberFromHtml']
    mcid=MemberCommonInformation.objects.get(home_no=houseno)

    mid=MemberDetails.objects.get(m_id=mcid)
    # email=request.POST['EmailFromHtml']
    # # user_id.email=email
    # mid=MemberDetails.objects.get(user_id.email==email)

    newpassword=request.POST['NewPasswordFromHtml']
    confirmpassword=request.POST['ConfirmNewPasswordFromHtml']

    if newpassword==confirmpassword:
        fname=request.POST['FNameFromHtml']
        lname=request.POST['LNameFromHtml']
        JobProfession=request.POST['JobFromHtml']
        Contact=request.POST['ContactNumberFromHtml']
        

        uid.password=newpassword
        uid.save()

        mid.fname=fname
        mid.lname=lname
        mid.m_id.contactno=Contact
        mid.m_id.job_profession=JobProfession

        if "ProfilePicFromHtml" in request.FILES:
            profilepicture=request.FILES['ProfilePicFromHtml']
            mid.profile_pic=profilepicture
            mid.save()

        mid.save()
        # mid=MemberDetails.objects.all()
        context={
            'uid':uid,
            'cid':cid,
            'mid':mid,
            'mcid':mcid,
            }
        s_msg="Successfully Upadated Member Info"
        return render(request,"chairman/m-profile.html",{'s_msg':s_msg,'context':context})
    else:
        e_msg="Password Not Match"
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"chairman/my-profile-page.html",{'e_msg':e_msg,'context':context})


def add_balance_fun(request):
    if request.POST:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        title=request.POST['title']
        amount=request.POST['amount']
        # due_date=request.POST['due_date']
        try:
            balanceid = Balance.objects.create(title=title,amount_have=amount)
        except:
            balanceid = Balance.objects.get(title=title)
            balanceid.amount_have += int(amount)
            balanceid.save() 
        balanceid = Balance.objects.all()
        context={
            "uid":uid,
            "cid":cid,
            "balanceid":balanceid,
            }
        return render(request,"chairman/Society-Balance.html",{"context":context})
    else:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        context={
            "uid":uid,
            "cid":cid,
        } 
        return render(request,"chairman/Add-Society-Balance.html",{"context":context})

def view_balance_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":         
        cid=Chairman.objects.get(user_id=uid)
        # maintenance_data=Maintenance.objects.filter(cid=cid.id)
        balanceid=Balance.objects.all()
        # expenseid=Expense.objects.all().order_by('-id')
        expenseid=Expense.objects.all().order_by('-id')
        context={
            "uid":uid,
            "cid":cid,
            "balanceid":balanceid,
            "expenseid":expenseid,
        }
        return render(request,"chairman/Society-Balance.html",{"context":context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        balanceid=Balance.objects.all()
        expenseid=Expense.objects.all().order_by('-id')
        context={
            "uid":uid,
            "cid":cid,
            "balanceid":balanceid,
            "expenseid":expenseid,
        }
        return render(request,"user/user-Society-balance.html",{"context":context})

def add_expense_fun(request):
    if request.POST:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        title=request.POST['title']
        BLtitle=request.POST['BLtitle']
        amount=request.POST['Price']
        # due_date=request.POST['due_date']
        # try:
        #     balanceid = Balance.objects.create(title=title,amount_have=amount)
        # except:
        #     balanceid = Balance.objects.get(title=title)
        #     balanceid.amount_have += int(amount)
        #     balanceid.save() 
        balanceid = Balance.objects.get(title=BLtitle)
        expenseid = Expense.objects.create(title=title,Price=amount)
        balanceid.amount_have -= int(amount)
        balanceid.save()
        balanceid=Balance.objects.all()
        expenseid=Expense.objects.all().order_by('-id')
        context={
            "uid":uid,
            "cid":cid,
            "balanceid":balanceid,
            'expenseid':expenseid,
            }
        return render(request,"chairman/Society-Balance.html",{"context":context})
    else:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        context={
            "uid":uid,
            "cid":cid,
            # 'balanceid':balanceid,
        } 
        return render(request,"chairman/Add-Expense.html",{"context":context})


# ----------------------member fun (profile show in chairman.index-page.member-list.onclickOf.ViewProfile)-------------------------------------------------------------
#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----



# payment START-----payment START-----payment START-----payment START-----payment START-----payment START-----payment START-----

def add_maintenance_fun(request):
    if request.POST:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        title=request.POST['title']
        amount=request.POST['amount']
        due_date=request.POST['due_date']
        # add maintenance of chairman
        Maintenance.objects.create(user_id=uid,cid=cid,title=title,amount=amount,due_date=due_date)
        # members 
        allmembers = MemberDetails.objects.all()
        for i in allmembers:
            mid  = MemberDetails.objects.get(id = i.id)
            Maintenance.objects.create(user_id=uid,member_id=mid,title=title,amount=amount,due_date=due_date)

        maintenance_data=Maintenance.objects.all()
        context={
            "uid":uid,
            "cid":cid,
            "maintenance_data":maintenance_data,
        }
        return render(request,"chairman/view-maintenance.html",{"context":context})
    else:
        uid=User.objects.get(email=request.session['c_email'])         
        cid=Chairman.objects.get(user_id=uid)
        context={
            "uid":uid,
            "cid":cid,
        } 
        return render(request,"chairman/add-maintenance.html",{"context":context})

def view_maintenance_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":         
        cid=Chairman.objects.get(user_id=uid)
        maintenance_data=Maintenance.objects.filter(cid=cid)
        context={
            "uid":uid,
            "cid":cid,
            "maintenance_data":maintenance_data,
        }
        return render(request,"chairman/view-maintenance.html",{"context":context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        maintenance_data=Maintenance.objects.filter(member_id=cid)
        context={
            "uid":uid,
            "cid":cid,
            "maintenance_data":maintenance_data,
        }
        return render(request,"user/view-maintenance.html",{"context":context})
    # uid=User.objects.get(email=request.session['c_email'])
    # cid=Chairman.objects.get(user_id=uid)
    # maintenance=Maintenance.objects.all()
    # context={
    #         'uid':uid,
    #         'cid':cid,
    #         'maintenance':maintenance,
    #         }
    # return render(request,"chairman/add-maintenance.html",{'context':context})

def payment_pay_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"payment/pay.html",{'context':context})
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"payment/pay.html",{'context':context})
    else:
        pass


def initiate_payment_fun(request):
    if request.method == "GET":
        # uid=User.objects.get(id=pk)

        uid=User.objects.get(email=request.session['c_email'])
        context={
            'uid':uid,
        }
        return render(request, 'payment/pay.html',{'context':context})
    try:
        # uid=User.objects.get(email=request.session['c_email'])
        # uid=User.objects.get(id=pk)
        balance=request.POST['title']
        username = request.POST['username']
        # password = request.POST['password']
        amount = int(request.POST['amount'])
        uid = User.objects.get(email=username)
    except:
        return render(request, 'payment/pay.html', context={'error': 'Wrong Accound Details or amount'})

    balanceid=Balance.objects.get(title=balance)
    balanceid.amount_have += int(amount)
    balanceid.save()
    transaction = Transaction.objects.create(made_by=uid, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY
    # email=uid.email

    # if uid.role=="user":
    #     maintenance_data=Maintenance.objects.get(member_id.user_id=uid)
    if uid.role=="chairman":
        cid=Chairman.objects.get(user_id=uid)
        try:

            maintenance_data=Maintenance.objects.get(cid=cid)
            if maintenance_data.amount==amount:
                maintenance_data.status = "paid"
                maintenance_data.save()
            else:
                # if maintenance_data.amount==amount
                maintenance_data.status = "Pending"
                maintenance_data.save()
        except:
            maintenance_data=Maintenance.objects.get(cid=cid,status="Pending")
            maintenance_data.status = "paid"
            maintenance_data.save()
    elif uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        try:
            maintenance_data=Maintenance.objects.get(member_id=cid)
            if maintenance_data.amount==amount:
                maintenance_data.status = "paid"
                maintenance_data.save()
            else:
                # if maintenance_data.amount==amount
                maintenance_data.status = "Pending"
                maintenance_data.save()
        except:
            maintenance_data=Maintenance.objects.get(member_id=cid,status="Pending")
            maintenance_data.status = "paid"
            maintenance_data.save()

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/home/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payment/redirect.html', context=paytm_params)



@csrf_exempt
def callback_fun(request):
    if request.method == 'POST':
        # uid=User.objects.get(email=email)
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payment/callback.html', context=received_data)
        return render(request, 'payment/callback.html', context=received_data)

# def callback_fun(request):
    

def all_payment_list_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Chairman.objects.get(user_id=uid)
    paymentid=Transaction.objects.all()
    mypayment=Transaction.objects.filter(made_by=uid)
    context={
            'uid':uid,
            'cid':cid,
            'paymentid':paymentid,
            'mypayment':mypayment,
            }
    return render(request,'payment/all-payment.html',{'context':context})
    if uid.role=="user":
        cid=MemberDetails.objects.get(user_id=uid)
        # paymentid=Transaction.objects.all()
        mypayment=Transaction.objects.filter(made_by=uid)
        context={
                'uid':uid,
                'cid':cid,
                # 'paymentid':paymentid,
                'mypayment':mypayment,
                }
        return render(request,'user/user-all-payment.html',{'context':context})


def user_all_payment_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=MemberDetails.objects.get(user_id=uid)
        # paymentid=Transaction.objects.all()
    mypayment=Transaction.objects.filter(made_by=uid)
    context={
            'uid':uid,
            'cid':cid,
                # 'paymentid':paymentid,
            'mypayment':mypayment,
            }
    return render(request,'user/user-all-payment.html',{'context':context})
# ===payment END=======payment END=======payment END=======payment END=======payment END=======payment END=======payment END=======payment END====












#-------------------------------------Member View(Start Here)---------------------------------------------------------->
#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START

# def user_index_fun(request):
#     if "c_email" in request.session:
#         uid=User.objects.get(email=request.session['c_email'])
#         mid=MemberDetails.objects.get(user_id=uid)
#         # mid=MemberDetails.objects.all()
#         context={
#             'uid':uid,
#             'mid':mid,
#             }
#         return render(request,"user/index.html",{'context':context})
#     else:
#         return render(request,"chairman/login.html")

def member_my_profile_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=MemberDetails.objects.get(user_id=uid)
    # noticedata=Notice.objects.all()
    context={
            'uid':uid,
            'cid':cid,
            # 'noticedata':noticedata,
            }
    return render(request,"user/member-my-profile-page.html",{'context':context})

def member_my_profile_update_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=MemberDetails.objects.get(user_id=uid)
    newpassword=request.POST['NewPasswordFromHtml']
    confirmpassword=request.POST['ConfirmNewPasswordFromHtml']

    if newpassword==confirmpassword:
        fname=request.POST['FNameFromHtml']
        lname=request.POST['LNameFromHtml']
        JobProfession=request.POST['JobFromHtml']
        Contact=request.POST['ContactNumberFromHtml']
        # houseno=request.POST['HouseNumberFromHtml']

        uid.password=newpassword
        cid.fname=fname
        cid.lname=lname
        # mid.m_id.home_no=houseno
        cid.m_id.job_profession=JobProfession

        if "ProfilePicFromHtml" in request.FILES:
            profilepicture=request.FILES['ProfilePicFromHtml']
            cid.profile_pic=profilepicture
            cid.save()

        cid.m_id.contactno=Contact
        uid.save()
        cid.save()
        cid.m_id.save()
        context={
            'uid':uid,
            # 'cid':cid,
            'cid':cid,
            }
        s_msg="Successfully Upadated"
        return render(request,"user/member-my-profile-page.html",{'s_msg':s_msg,'context':context})
    else:
        e_msg="Password Not Match"
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"user/member-my-profile-page.html",{'e_msg':e_msg,'context':context})

# def my_personal_chat_user_fun(request):
#     uid=User.objects.get(email=request.session['c_email'])
#     cid=MemberDetails.objects.get(user_id=uid)
    
#     chatid=chat.objects.get(recevier=cid.user_id.email)
#     # chatid=chat.objects.all()
#     senderfulldetails=User.objects.get(email=chatid.sender)
    
#     sendermemberdetails=Chairman.objects.get(user_id=senderfulldetails)
#     # myemail=cid.user_id.email
#     # chatreceiveremail = chatid.recevier
#     # if myemail==chatreceiveremail:
#     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",chatid.recevier)
#     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",chatid.sender)
#     print("--------------------------------------------",senderfulldetails.email)
#     print("--------------------------------------------",sendermemberdetails.fname)
#     context={
#         'chatid':chatid,
#         'uid':uid,
#         'cid':cid,
#         'sendermemberdetails':sendermemberdetails,
#         # 'memberdata':memberdata,
#                 # 'mid':mid,
#         }
#     return render(request,"user/my-msg.html",{'context':context})

# def reply_send_msg_fun(request):
#     uid=User.objects.get(email=request.session['c_email'])
#     if uid.role=="chairman":
#         cid=Chairman.objects.get(user_id=uid)
#         sender = cid.user_id.email
#         recevier=request.POST['userid']
#         message=request.POST['typemsgFromHTML']
#         chatid = chat.objects.create(sender=sender,recevier=recevier,msg=message)
#         # notify.send(sender, recipient=recevier, verb='Message', description=request.POST.get('message'))
#         userdata=User.objects.get(email=recevier)
#         memberdata=MemberDetails.objects.get(user_id=userdata)
#         print("fffffffffffffffffffffffffffffffffff",recevier)
#         context={
#                 'chatid':chatid,
#                 'uid':uid,
#                 'cid':cid,
#                 'memberdata':memberdata,
#                 # 'mid':mid,
#                 }
#         return render(request,"chairman/chariman-chat.html",{'context':context})
#     if uid.role=="user":
#         cid=MemberDetails.objects.get(user_id=uid)
#         sender = cid.user_id.email
#         recevier=request.POST['userid']
#         message=request.POST['replyFromHTML']
#         chatid = chat.objects.create(sender=sender,recevier=recevier,msg=message)
#         # notify.send(sender, recipient=recevier, verb='Message', description=request.POST.get('message'))
#         userdata=User.objects.get(email=recevier)
#         memberdata=MemberDetails.objects.get(user_id=userdata)
#         print("fffffffffffffffffffffffffffffffffff",recevier)
#         context={
#                 'chatid':chatid,
#                 'uid':uid,
#                 'cid':cid,
#                 'memberdata':memberdata,
#                 # 'mid':mid,
#                 }
#         return render(request,"chairman/chariman-chat.html",{'context':context})
    
    # else:
    #     pass
    # sender = cid.user_id.email
    # recevier=request.POST['userid']
    # message=request.POST['typemsgFromHTML']
    # chatid = chat.objects.create(sender=sender,recevier=recevier,msg=message)
    #     # notify.send(sender, recipient=recevier, verb='Message', description=request.POST.get('message'))
    # userdata=User.objects.get(email=recevier)
    # memberdata=MemberDetails.objects.get(user_id=userdata)
    # context={
    #     'chatid':chatid,
    #     'uid':uid,
    #     'cid':cid,
    #     'memberdata':memberdata,
    #             # 'mid':mid,
    #     },{'context':context}


def member_my_notice_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=MemberDetails.objects.get(user_id=uid)
    noticedata=Notice.objects.filter(uploaded_by=cid.fname)
    context={
            'uid':uid,
            'cid':cid,
            'noticedata':noticedata,
            }
    return render(request,"user/my-notice.html",{'context':context}) 

def member_my_post_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=MemberDetails.objects.get(user_id=uid)
    # noticedata=Notice.objects.filter(uploaded_by=cid.fname)
    pid=Post.objects.filter(uploaded_by=cid.fname)
    context={
            'uid':uid,
            'cid':cid,
            'pid':pid,
            # 'noticedata':noticedata,
            }
    return render(request,"user/my-post.html",{'context':context}) 


#-------------------------------------Member View(END Here)---------------------------------------------------------->
#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----


#-------------------------------------WATCHMAN View(Start Here)---------------------------------------------------------->
#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START


def watchman_my_profile_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Watchman.objects.get(user_id=uid)
    # noticedata=Notice.objects.all()
    context={
            'uid':uid,
            'cid':cid,
            # 'noticedata':noticedata,
            }
    return render(request,"watchman/watchman-my-profle-page.html",{'context':context})

def profile_update_watchman_fun(request):
    uid=User.objects.get(email=request.session['c_email'])
    cid=Watchman.objects.get(user_id=uid)
    newpassword=request.POST['NewPasswordFromHtml']
    confirmpassword=request.POST['ConfirmNewPasswordFromHtml']

    if newpassword==confirmpassword:
        fname=request.POST['FNameFromHtml']
        lname=request.POST['LNameFromHtml']
        Contact=request.POST['ContactNumberFromHtml']

        uid.password=newpassword
        cid.fname=fname
        cid.lname=lname
        # mid=MemberCommonInformation.objects.get(home_no=houseno)
        # mid.job_profession=JobProfession

        if "ProfilePicFromHtml" in request.FILES:
            profilepicture=request.FILES['ProfilePicFromHtml']
            cid.profile_pic=profilepicture
            cid.save()

        cid.contactno=Contact
        uid.save()
        cid.save()
        # mid.save()
        context={
            'uid':uid,
            'cid':cid,
            # 'mid':mid,
            }
        s_msg="Successfully Upadated"
        return render(request,"watchman/watchman-my-profle-page.html",{'s_msg':s_msg,'context':context})
    else:
        e_msg="Password Not Match"
        context={
            'uid':uid,
            'cid':cid,
            }
        return render(request,"watchman/watchman-my-profle-page.html",{'e_msg':e_msg,'context':context})


#-------------------------------------WATCHMAN View(END Here)---------------------------------------------------------->
#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----END-----#-----






#-------------------------------------AJAX AJAX AJAX AJAX(Start Here)---------------------------------------------------------->
#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START-----#-----START

def add_watchman_ajax_fun(request):
        role=request.POST['role']
        email=request.POST['email']
        password=request.POST['password']
        fname=request.POST['fname']
        lname=request.POST['lname']
        mobileno=request.POST['mobileno']
        isactive="True"

        print("--------------success django----------------",email)
        userdata=User.objects.create(email=email,password=password,is_active=isactive,role=role,otp="1234",created_at="not provided",updated_at="not provided")
        userdata.save()
        # userdata=User.objects.all()


        watchmandata=Watchman.objects.create(user_id=userdata,fname=fname,lname=lname,contactno=mobileno)
        watchmandata.save()

        userdata=User.objects.values()
        userdata = list(userdata)
        watchmandata=Watchman.objects.values()
        watchmandata = list(watchmandata)
        # wid=Watchman.objects.all()
        print("--------------success----------------")
        context={
            "msg":"success",
            'userdata':userdata,
            "watchmandata":watchmandata,
            # "uid":uid,
        }
        return JsonResponse({"context":context})
        # return render(request,"chairman/login.html",{'context':context})
        # context={
        #         'uid':uid,
        #         'userdata':userdata,
        #         'wid':wid,
        #         }
        # s_msg="Added Successfully(wait for Chairman Approval)"
        # sendmail("Forgot - Password","Email-template-send-OTP",'ppoojan40@gmail.com',{'wid':wid})
        # return render(request,"chairman/register.html",{'s_msg':s_msg,'context':context})


def watchman_approval_ajax_fun(request):
    id = request.POST['id']

    wid=Watchman.objects.get(id=id)
    # uid=User.objects.get(id=id)
    # wid=Watchman.objects.get(user_id=uid)

    wid.user_id.is_verified = "True"
    wid.save()
    wid.user_id.save()
    # uid.save()
    
    uid=User.objects.get(email=wid.user_id.email)
    wid=Watchman.objects.values()
    uid=User.objects.values()
    
    wid = list(wid)
    uid = list(uid)
    print("--------------success----------------")
    context={
        "wid":wid,
        "uid":uid,
        }
    return JsonResponse({"context":context})