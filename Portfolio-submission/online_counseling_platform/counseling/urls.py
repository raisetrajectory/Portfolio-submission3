# counseling/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_session, chat_view, send_message # type: ignore

urlpatterns = [
    path('', views.home, name='home'),  # ホームビューのルーティング # type: ignore
    path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'), # type: ignore
    path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'), # type: ignore
    path('signup/', views.signup, name='signup'), # type: ignore
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 新しいURLパターンを追加
    path('create_session/', create_session, name='create_session'),
    path('chat/<int:session_id>/', chat_view, name='chat_view'),
    path('send_message/', send_message, name='send_message'),

    # 他のURLパターン
]
