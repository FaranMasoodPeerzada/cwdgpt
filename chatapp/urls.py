from django.urls import path
from . import views

urlpatterns= [

    path('asd', views.chat_list, name='chat-list'),
    path('get_chat_messages/<int:conversation_id>/', views.get_chat_messages, name='get-chat-messages'),
    path('',views.register,name='registeration'),
    #path('start-chat/', views.start_chat, name='start_chat'),
    path('chat/<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('delete-conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('conversations/', views.conversations_list, name='conversations_list'),
    path('home',views.home,name='home'),
     path('delete-chat/<int:conversation_id>/', views.user_delete_chat, name='user_delete_chat'),
    # path('home/<int:conversation_id>/',views.message_list,name='message_list'),
    path('signup',views.handlesignup,name='signup'),
    path('login-page',views.loginpage,name='login-page'),
    path('login',views.handleuserlogin,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('admin-login',views.adminlogin,name='admin-login'),
    path('admin-login-processing',views.handleadminlogin,name='admin-login-processing'),
    path('change_password',views.PasswordChangeView.as_view(),name='change-password'),
     path('password_success',views.password_success,name='password_success'),
   
    
    path('admin-logout',views.admin_logout,name='admin-logout'),
    path('admin-panel',views.adminpanel,name='admin-panel'),
    
    path('admin-chats/<int:conversation_id>/', views.adminchats, name='admin-chats'),
    path('user/<int:user_id>/', views.user_chats_detail, name='user_chats_detail'),
    path('userchat/<int:conversation_id>/<int:user_id>/', views.userchatview, name='user_chat_view'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('deleted/<int:user_id>/', views.delete_applicant, name='delete_applicant'),
    path('deleteuser/<int:id>/', views.delete_user, name='delete_user'),
  
]
handler404='chatapp.views.handling404'
