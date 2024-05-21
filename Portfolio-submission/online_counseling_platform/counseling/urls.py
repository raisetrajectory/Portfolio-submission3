# counseling/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('counselor/<int:pk>/', views.counselor_profile, name='counselor_profile'), # type: ignore
    path('counselor/<int:pk>/edit/', views.edit_counselor_profile, name='edit_counselor_profile'), # type: ignore
    path('signup/', views.signup, name='signup'), # type: ignore
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 他のURLパターン
]
