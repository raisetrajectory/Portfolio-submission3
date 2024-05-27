# counseling/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_session, chat_view, send_message, session_detail # type: ignore

# urlpatterns = [
#     path('', views.home, name='home'),  # ホームビューのルーティング # type: ignore
#     path('signup/', views.signup, name='signup'), # type: ignore
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('chat/', views.chat_view, name='chat'),  # チャット画面のURL
#     path('logout/', views.logout_view, name='logout'),  # ログアウト機能の追加
#     path('profile/', views.profile_view, name='profile'),  # プロフィール画面の追加 # type: ignore
#     path('counselors/', views.counselor_list_view, name='counselor_list'),  # カウンセラー一覧画面の追加 # type: ignore
#     path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'), # type: ignore
#     path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'), # type: ignore
#     # path('create_session/', create_session, name='create_session'),
#     path('create_session/', views.create_session, name='create_session'),
#     # path('chat/<int:session_id>/', chat_view, name='chat_view'),
#     path('chat/<int:session_id>/', views.chat_view, name='chat_view')
#     path('chat/<int:counselor_id>/', views.chat_view, name='chat'),
#     path('profile/<int:counselor_id>/', views.profile_view, name='profile'),  # カウンセラーIDに基づくプロフィールビュー
#     # path('send_message/', send_message, name='send_message'),
#     path('send_message/', views.send_message, name='send_message'),
#     # path('session/<int:session_id>/', session_detail, name='session_detail'),
#     path('session/<int:session_id>/', views.session_detail, name='session_detail'),
# ]

urlpatterns = [
    path('', views.home, name='home'),  # ホームビューのルーティング
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('chat/', views.chat, name='chat'),  # チャット画面のURL
    path('logout/', views.logout_view, name='logout'),  # ログアウト機能の追加
    path('profile/', views.profile_view, name='profile'),  # プロフィール画面の追加
    path('counselors/', views.counselor_list_view, name='counselor_list'),  # カウンセラー一覧画面の追加
    path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'),
    path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'),
    path('create_session/', create_session, name='create_session'),
    path('chat/<int:counselor_id>/', views.chat_view, name='chat_view'),  # カウンセラーごとのチャット画面
    path('send_message/', send_message, name='send_message'),
    path('session/<int:session_id>/', session_detail, name='session_detail'),
    path('profile/<int:counselor_id>/', views.profile_view, name='profile'),  # カウンセラーごとのプロフィール画面
]