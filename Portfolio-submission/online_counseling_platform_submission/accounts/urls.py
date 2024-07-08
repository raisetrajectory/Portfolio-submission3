from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist/', views.regist, name='regist'),
    path('counselor_regist/', views.counselor_regist, name='counselor_regist'),
    path('counselor_login/', views.counselor_login, name='counselor_login'),
    path('activate_user/<uuid:token>/', views.activate_user, name='activate_user'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_edit/', views.user_edit, name='user_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('counselor_profile/', views.counselor_profile, name='counselor_profile')
]
