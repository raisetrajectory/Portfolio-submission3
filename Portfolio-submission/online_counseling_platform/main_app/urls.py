from django.urls import path
from . import views

app_name = 'main_app'
app_name = 'counseling' #6月12日追加

urlpatterns = [
    path('create_theme/', views.create_theme, name='create_theme'), # type: ignore
    path('list_themes/', views.list_themes, name='list_themes'), # type: ignore
    path('edit_theme/<int:id>/', views.edit_theme, name='edit_theme'), # type: ignore
    path('delete_theme/<int:id>/', views.delete_theme, name='delete_theme'), # type: ignore
    path('post_comments/<int:theme_id>/', views.post_comments, name='post_comments'), # type: ignore
    path('save_comment/', views.save_comment, name='save_comment'), # type: ignore
]