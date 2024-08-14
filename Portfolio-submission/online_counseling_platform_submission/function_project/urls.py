from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import show_error_page
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('accounts:user_login', permanent=False)),  # リダイレクト先を'user_login'に変更
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('boards/', include('boards.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debugモードの時に静的ファイルとメディアファイルを提供する設定を追加
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

# カスタム404エラーページのハンドラーを設定
handler404 = show_error_page