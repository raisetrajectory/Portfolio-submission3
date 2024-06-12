from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from counseling.views import show_error_page # type: ignore #2024年6月12日追加

# app_name = main_app #2024年6月12日追加

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauthのルーティングを追加
    path('', include('counseling.urls')),  # counselingアプリのルーティングを追加
    path('logout/', LogoutView.as_view(), name='logout'),  # ログアウト機能の追加
    path('counseling/', include('counseling.urls')),
    path('main_app/', include('main_app.urls')),
]
handler404 = show_error_page #2024年6月12日追加

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)