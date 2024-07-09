from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('create_theme/', views.create_theme, name='create_theme'),
    path('list_themes/', views.list_themes, name='list_themes'),
    path('edit_theme/<int:id>/', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:id>/', views.delete_theme, name='delete_theme'),
    path('post_comments/<int:theme_id>/', views.post_comments, name='post_comments'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('counselor_list/', views.counselor_list, name='counselor_list'),
    # path('counselor_profile/<int:counselor_id>/', views.counselor_profile, name='counselor_profile'),
    path('counselor_profile/', views.counselor_profile, name='counselor_profile'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),
    path('upload_sample/', views.upload_sample, name='upload_sample'),
    path('upload_model_form/', views.upload_model_form, name='upload_model_form'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),

    path('select_counselor/<int:counselor_id>/', views.select_counselor, name='select_counselor'),
    # path('deselect_counselor/', views.deselect_counselor, name='deselect_counselor'),
]
