from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauthのルーティングを追加
    path('', include('counseling.urls')),  # counselingアプリのルーティングを追加
]
