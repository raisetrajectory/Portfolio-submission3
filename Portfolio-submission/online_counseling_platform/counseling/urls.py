# counseling/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_session, chat_view, send_message, session_detail # type: ignore

urlpatterns = [
    path('', views.home, name='home'),  # ホームビューのルーティング # type: ignore
    path('signup/', views.signup, name='signup'), # type: ignore
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('chat/', views.chat_view, name='chat'),  # チャット画面のURL

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'), # type: ignore
    path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'), # type: ignore
    path('create_session/', create_session, name='create_session'),
    path('chat/<int:session_id>/', chat_view, name='chat_view'),
    path('send_message/', send_message, name='send_message'),
    path('session/<int:session_id>/', session_detail, name='session_detail'),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'), # type: ignore
    # path('chat/', views.chat, name='chat'), # type: ignore
    # path('profile/', views.profile, name='profile'), # type: ignore
    # path('counselor-list/', views.counselor_list, name='counselor_list'), # type: ignore
]
