from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import show_error_page
from django.shortcuts import redirect
from django.conf.urls import handler404

urlpatterns = [
    path('', lambda request: redirect('accounts:user_login', permanent=False)),  # リダイレクト先を'user_login'に変更
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('boards/', include('boards.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Debugモードの時に静的ファイルとメディアファイルを提供する設定を追加
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     # DEBUG = Falseの場合、これが必要です。
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# DEBUG = Trueの場合は、メディアファイルと静的ファイルの提供を設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
else:
    # DEBUG = Falseの場合の設定を追加する必要があります。
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# DEBUG = False の時にカスタム404エラーページを表示
handler404 = show_error_page
