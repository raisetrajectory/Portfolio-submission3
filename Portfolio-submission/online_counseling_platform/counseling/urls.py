# counseling/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_session, chat_view, send_message, session_detail, delete_message  # 追加
from counseling.forms import CustomAuthenticationForm
from django.conf import settings #2024年6月4日追加
from django.conf.urls.static import static #2024年6月4日追加

# app_name = 'counseling' #6月12日追加

urlpatterns = [
    path('', views.home, name='home'),  # ホームビューのルーティング # type: ignore
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('chat/', views.chat_view, name='chat'),  # チャット画面のURL
    path('logout/', views.logout_view, name='logout'),  # ログアウト機能の追加
    path('profile/', views.profile_view, name='profile'),  # プロフィール画面の追加
    path('counselors/', views.counselor_list_view, name='counselor_list'),  # カウンセラー一覧画面の追加
    path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'),
    path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'),
    path('create_session/', views.create_session, name='create_session'),
    path('chat/<int:session_id>/', views.chat_view, name='chat_view'),
    path('chat/<int:counselor_id>/', views.chat_view, name='chat'),
    path('profile/<int:counselor_id>/', views.profile_view, name='profile'),  # カウンセラーIDに基づくプロフィールビュー
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('chat/session/<int:session_id>/', views.chat_view, name='chat_session'),
    path('chat/counselor/<int:counselor_id>/', views.chat_view, name='chat_counselor'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('chat/', views.chat_view, name='chat_view'),

    path('upload_sample/', views.upload_sample, name='upload_sample'), #2024年6月5日追加
    path('profile/', views.profile, name='profile'),#2024年6月6日追加

    path('chat/<int:counselor_id>/start/', chat_view, name='chat_start'),
    path('send_message/', send_message, name='send_message'),
    path('chat/<int:session_id>/', chat_view, name='chat_view'),

    path('', views.home, name='home'), #6月12日追加
    path('regist/', views.regist, name='regist'), #6月12日追加
    path('activate_user/<uuid:token>/', views.activate_user, name='activate_user'), #6月12日追加
    path('user_login/', views.user_login, name='user_login'), #6月12日追加
    path('user_logout/', views.user_logout, name='user_logout'), #6月12日追加
    path('user_edit/', views.user_edit, name='user_edit'), #6月12日追加
    path('change_password/', views.change_password, name='change_password'), #6月12日追加
    # path('home2/', views.home, name='home2'),  # counselingアプリケーション用のURLパターン　#6月13日追加 不要の場合は削除して大丈夫です！
    path('base/', views.base, name='base'),  # 新しいURLパターンを追加

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
