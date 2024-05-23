from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauthのルーティングを追加
    path('', include('counseling.urls')),  # counselingアプリのルーティングを追加
    path('logout/', LogoutView.as_view(), name='logout'),  # ログアウト機能の追加
]
