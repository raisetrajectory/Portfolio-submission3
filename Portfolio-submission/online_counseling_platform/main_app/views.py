from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage  # チャットメッセージのモデルをインポート
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .models import CounselingSession, ChatMessage, User

from django.shortcuts import render, redirect, get_object_or_404 #6月12日追加
from . import forms #6月12日追加
from django.contrib import messages #6月12日追加
from .models import Themes, Comments #6月12日追加
from django.http import Http404 #6月12日追加
from django.core.cache import cache #6月12日追加
from django.http import JsonResponse #6月12日追加

def create_theme(request): #6月追加
        create_theme_form = forms.CreateThemeForm(request.POST or None)
        if create_theme_form.is_valid():
            create_theme_form.instance.user = request.user
            create_theme_form.save()
            messages.success(request, '掲示板を作成しました。')
            # return redirect('list_themes')
            # return redirect('home')
        return render(
        request, 'create_theme.html', context={
            'create_theme_form': create_theme_form,
        }
    )

def list_themes(request): #6月追加
    themes = Themes.objects.fetch_all_themes() # type: ignore
    return render(
        request, 'list_themes.html', context={
            'themes': themes
        }
    )

def edit_theme(request, id): #6月追加
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました。')
        return redirect('list_themes')
    return render(
        request, 'edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )

def delete_theme(request, id): #6月追加
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid(): # csrf check
        theme.delete()
        messages.success(request, '掲示板を削除しました。')
        return redirect('list_themes')
    return render(
        request, 'delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )

def post_comments(request, theme_id): #6月追加
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
        return redirect('post_comments', theme_id= theme_id)
    return render(
        request, 'post_comments.html', context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )

def save_comment(request): #6月追加
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return JsonResponse({'message': '一時保存しました！'})
    return JsonResponse({'message': 'エラーが発生しました。'})


def home(request):
    return render(request, 'home.html')

def login_view(request):
    # ログインのロジック
    return render(request, 'login.html')

@login_required
def chat_view(request, session_id=None):
    if session_id:
        session = get_object_or_404(CounselingSession, id=session_id)
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
        return render(request, 'chat.html', {'session': session, 'messages': messages})
    else:
        messages = ChatMessage.objects.all()  # チャットメッセージを取得
        try:
            get_template('counseling/registration/chat.html')
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist("The template 'counseling/registration/chat.html' does not exist.")
        return render(request, 'counseling/registration/chat.html', {'messages': messages})

def logout_view(request):
    # ログアウトのロジック
    logout(request)  # Djangoのlogout関数を使用してユーザーをログアウトさせる
    return redirect('home')  # ログアウト後にホームページにリダイレクト

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        message = request.POST.get('message')
        session = get_object_or_404(CounselingSession, id=session_id)
        ChatMessage.objects.create(session=session, sender=request.user, message=message)
        return JsonResponse({'status': 'success'})


