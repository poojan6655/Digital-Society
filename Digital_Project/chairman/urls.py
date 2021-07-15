"""Digital_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from chairman import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.chairman_fun, name='chairmanpage'),
    path('login/', views.login_fun, name='login-page'),
    # path('login-evalute/', views.login_evalute, name='login-evalute'),
    path('registration/', views.registration_fun, name='registration-page'),
    # path('registration-evalute/', views.registration_evalute_fun, name='registration-evalute-page'),
    path('logout/', views.logout_fun, name='logout-page'),
    path('forgot-password/', views.forgot_password_fun, name='forgot-password-page'),
    path('send-OTP/', views.send_OTP_fun, name='send-OTP'),
    path('OTP-Receive/', views.OTP_Receive_fun, name='OTP-Receive'),
    path('reset-password/', views.Reset_Password_fun, name='Reset-Password'),
    path('add-notice/', views.add_notice_fun, name='add-notice-page'),
    # path('notice-added/', views.notice_added_fun, name='notice-added-page'),
    path('view-notice/', views.view_notice_fun, name='view-notice-page'),
    path('delete-notice/<int:pk>', views.delete_notice_fun, name='delete-notice-page'),
    path('calendar/', views.calendar_fun, name='calendar-page'),
    path('add-post/', views.add_post_fun, name='add-post-page'),
    # path('post-added/', views.post_added_fun, name='post-added-page'),
    path('view-post/', views.view_post_fun, name='view-post-page'),
    path('delete-post/<int:pk>', views.delete_post_fun, name='delete-post-page'),
    path('my-profile/', views.my_profile_fun, name='my-profile-page'),
    path('profile-update/', views.profile_update_fun, name='profile-update-page'),
    path('add-member/', views.add_member_fun, name='add-member-page'),
    path('add-family-member/', views.add_family_member_fun, name='add-family-member-page'),
    path('member-added/', views.member_added_fun, name='member-added-page'),
    path('member-list/', views.member_list_fun, name='member-list-page'),
    path('my-society/', views.my_society_fun, name='my-society-page'),
    path('All-images-collection/', views.All_images_collection_fun, name='All-images-collection-page'),
    path('All-videos-collection/', views.All_videos_collection_fun, name='All-video-collection-page'),
    # path('chairman-chat/<int:pk>', views.chairman_chat_fun, name='chairman-chat-page'),
    # path('send-msg/', views.send_msg_page_fun, name='send-msg-page'),
    path('family-member-list/<int:pk>', views.family_member_list_fun, name='family-member-list-page'),
    path('watchman-list-approval/', views.watchman_list_approval_fun, name='watchman-list-approval-page'),
    path('watchman-approval/<int:pk>', views.watchman_approval_fun, name='watchman-approval-page'),
    path('add-maintenance/', views.add_maintenance_fun, name='add-maintenance-page'),
    path('view-maintenance/', views.view_maintenance_fun, name='view-maintenance-page'),
    path('add-balance/', views.add_balance_fun, name='add-balance-page'),
    path('view-balance/', views.view_balance_fun, name='view-balance-page'),

    path('add-expense/', views.add_expense_fun, name='add-expense-page'),
    # ------------------payment-------------------------------------
    path('payment-pay/', views.payment_pay_fun, name='payment-pay-page'),
    path('initiate-payment/', views.initiate_payment_fun, name='initiate-payment-page'),
    path('callback/', views.callback_fun, name='callback-page'),
    path('all-payment-list/', views.all_payment_list_fun, name='all-payment-list-page'),

    # ===================payment-END----------------------------------


    # --------------------AJAX START------------------------------
    path('add-watchman-ajax/', views.add_watchman_ajax_fun, name='add-watchman-ajax-page'),
    path('watchman-approval-ajax/', views.watchman_approval_ajax_fun, name='watchman-approval-ajax-page'),
    #----------------------AJAX END--------------------------------------


    #-------------START-------member profile comes for chairman, dynamically in view profile----------------------------------------
    path('chairman-member-profile/<int:pk>', views.chairman_member_profile_fun, name='chairman-member-profile-page'),
    path('chairman-member-profile-update/', views.chairman_member_profile_update_fun, name='chairman-member-profile-update-page'),
    #-------------END-------member profile comes for chairman, dynamically in view profile------------------------------------------


    #--------START-----------member profile comes for member in members login-------------------------------------------------------
    path('member-my-profile/', views.member_my_profile_fun, name='member-my-profile-page'),
    path('member-my-profile-update/', views.member_my_profile_update_fun, name='member-my-profile-update-page'),
    path('member-my-post/', views.member_my_post_fun, name='my-post-page'),
    path('member-my-notice/', views.member_my_notice_fun, name='my-notice-page'),
    # path('my-personal-chat-user/', views.my_personal_chat_user_fun, name='my-personal-chat-user-page'),
    # path('reply-send-msg/', views.reply_send_msg_fun, name='reply-send-msg-page'),
    path('user-all-payment/', views.user_all_payment_fun, name='user-all-payments'),
    # path('index-page-user/', views.user_index_fun, name='userpage'),
    #---------END----------member profile comes for member in members login-----------------------------------------------------------


    #--------START-----------WATCHMAN profile comes for WATCHMAN in WATCHMAN login-------------------------------------------------------
    path('watchman-my-profile/', views.watchman_my_profile_fun, name='watchman-my-profile-page'),
    path('profile-update-watchman/', views.profile_update_watchman_fun, name='profile-update-watchman-page'),
]
