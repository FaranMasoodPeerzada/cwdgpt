from django.urls import path
from . import views

urlpatterns= [

    path('',views.register,name='registeration'),
    #path('start-chat/', views.start_chat, name='start_chat'),
    path('chat/<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('delete-conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('conversations/', views.conversations_list, name='conversations_list'),
    path('home',views.home,name='home'),
    # path('home/<int:conversation_id>/',views.message_list,name='message_list'),
    path('signup',views.handlesignup,name='signup'),
    path('login-page',views.loginpage,name='login-page'),
    path('login',views.handlelogin,name='login'),
    path('logout',views.handlelogout,name='logout'),
    path('admin-panel',views.adminlogin,name='admin-panel'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('deleted/<int:user_id>/', views.delete_applicant, name='delete_applicant'),
    path('deleteuser/<int:id>/', views.delete_user, name='delete_user'),
  
]
