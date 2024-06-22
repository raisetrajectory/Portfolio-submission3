from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
from .models import Themes, Comments, Counselors

import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from boards.forms import PostCommentForm
from boards.forms import PostCommentForm, CreateThemeForm, DeleteThemeForm

# def home(request):
#     themes = Themes.objects.all()
#     comments = Comments.objects.filter(themes=themes)   # 必要に応じてクエリを修正します
#     post_comment_form = PostCommentForm()
#     context = {
#         'themes': themes,
#         'comments': comments,
#         'post_comment_form': post_comment_form,
#     }
#     return render(request, 'accounts/home.html', context)

def home(request):
    if request.method == 'POST':
        if 'create_theme' in request.POST:
            create_theme_form = CreateThemeForm(request.POST)
            if create_theme_form.is_valid():
                create_theme_form.instance.user = request.user
                create_theme_form.save()
                messages.success(request, '掲示板を作成しました。')
                return redirect('home')
        elif 'edit_theme' in request.POST:
            theme_id = request.POST.get('theme_id')
            theme = get_object_or_404(Themes, id=theme_id)
            if theme.user.id != request.user.id:
                raise Http404
            edit_theme_form = CreateThemeForm(request.POST, instance=theme)
            if edit_theme_form.is_valid():
                edit_theme_form.save()
                messages.success(request, '掲示板を更新しました。')
                return redirect('home')
        elif 'delete_theme' in request.POST:
            theme_id = request.POST.get('theme_id')
            theme = get_object_or_404(Themes, id=theme_id)
            if theme.user.id != request.user.id:
                raise Http404
            delete_theme_form = DeleteThemeForm(request.POST)
            if delete_theme_form.is_valid():
                theme.delete()
                messages.success(request, '掲示板を削除しました。')
                return redirect('home')
        elif 'post_comment' in request.POST:
            theme_id = request.POST.get('theme_id')
            theme = get_object_or_404(Themes, id=theme_id)
            saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
            post_comment_form = PostCommentForm(request.POST, initial={'comment': saved_comment})
            comments = Comments.objects.filter(theme=theme)
            if post_comment_form.is_valid():
                if not request.user.is_authenticated:
                    raise Http404
                post_comment_form.instance.theme = theme
                post_comment_form.instance.user = request.user
                post_comment_form.save()
                cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
                return redirect('home')
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comments, id=comment_id)
            if request.user != comment.user:
                raise Http404
            if request.method == 'POST':
                theme_id = comment.theme.id
                theme = get_object_or_404(Themes, id=theme_id)
                comment.delete()
                messages.success(request, 'コメントを削除しました。')
                return redirect('home')

    themes = Themes.objects.all()
    comments = Comments.objects.filter(theme__in=themes)
    post_comment_form = PostCommentForm()
    create_theme_form = CreateThemeForm()
    edit_theme_form = CreateThemeForm()
    delete_theme_form = DeleteThemeForm()

    context = {
        'themes': themes,
        'comments': comments,
        'post_comment_form': post_comment_form,
        'create_theme_form': create_theme_form,
        'edit_theme_form': edit_theme_form,
        'delete_theme_form': delete_theme_form,
    }
    return render(request, 'accounts/home.html', context)

def create_theme(request):
        create_theme_form = forms.CreateThemeForm(request.POST or None)
        if create_theme_form.is_valid():
            create_theme_form.instance.user = request.user
            create_theme_form.save()
            messages.success(request, '掲示板を作成しました。')
            return redirect('boards:list_themes')
        return render(
        request, 'boards/create_theme.html', context={
            'create_theme_form': create_theme_form,
        }
    )

def list_themes(request):
    themes = Themes.objects.fetch_all_themes() # type: ignore
    return render(
        request, 'boards/list_themes.html', context={
            'themes': themes
        }
    )

def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました。')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )

def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid(): # csrf check
        theme.delete()
        messages.success(request, '掲示板を削除しました。')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )

def post_comments(request, theme_id):
    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
    post_comment_form = forms.PostCommentForm(request.POST or None, initial={'comment': saved_comment})     # type: ignore
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme_id) # type: ignore
    if post_comment_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        post_comment_form.instance.theme = theme
        post_comment_form.instance.user = request.user
        post_comment_form.save()
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
        return redirect('boards:post_comments', theme_id= theme_id)
    return render(
        request, 'boards/post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )

def save_comment(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return JsonResponse({'message': '一時保存しました！'})
    return JsonResponse({'message': 'エラーが発生しました。'})

def counselor_list(request):
    counselors = Counselors.objects.all()
    return render(request, 'boards/counselor_list.html', {'counselors': counselors})

def counselor_profile(request):
    counselors = Counselors.objects.all()
    return render(request, 'boards/counselor_profile.html', {'counselors': counselors})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.user != comment.user:
        raise Http404
    if request.method == 'POST':
        theme_id = comment.theme.id
        theme = get_object_or_404(Themes, id=theme_id)  # テーマが存在するか確認
        comment.delete()
        messages.success(request, 'コメントを削除しました。')
        return redirect('boards:post_comments', theme_id=theme_id)
    return render(request, 'boards/delete_comment.html', context={'comment': comment})

def upload_sample(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        # 送られたファイルの取り出し
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage() # ファイルを保存する
        file_path = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(file_path)
        return  render(request, 'boards/upload_file.html', context={
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'boards/upload_file.html')

# def upload_sample(request):
#     if request.method == 'POST' and request.FILES['upload_file']:
#         # 送られたファイルの取り出し
#         upload_file = request.FILES['upload_file']
#         fs = FileSystemStorage() # ファイルを保存する
#         file_path = fs.save(upload_file.name, upload_file)
#         uploaded_file_url = fs.url(file_path)
#         return  render(request, 'boards/counselor_profile.html', context={
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'boards/counselor_profile.html')

def upload_model_form(request):
    user = None
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES) # type: ignore
        if form.is_valid():
            user = form.save()
    else:
        form = forms.UserForm() # type: ignore
    return render(request, 'boards/upload_model_form.html', context={
        'form': form, 'user': user
    })
