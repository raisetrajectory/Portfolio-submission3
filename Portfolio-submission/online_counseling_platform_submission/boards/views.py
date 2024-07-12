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

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import Comments
from .forms import PostCommentForm

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Counselors
from accounts.models import Counselor, Users

@login_required #記載内容のバックアップです！
def counselor_list(request):
    user = request.user
    if isinstance(user, Counselor):
        user_type = 'Counselor'
    else:
        user_type = 'User'
    counselors = Counselor.objects.all()
    context = {
        'counselors': counselors,
        'user_type': user_type,
        'current_user_email': user.email,  # ログインユーザーのメールアドレスをコンテキストに追加
    }
    return render(request, 'boards/counselor_list.html', context)

# @login_required
# def counselor_list(request):
#     if isinstance(request.user, Counselor):
#         user_type = 'Counselor'
#     else:
#         user_type = 'User'
#     counselors = Counselor.objects.all()
#     return render(request, 'boards/counselor_list.html', {'counselors': counselors, 'user_type': user_type,})

@login_required
def select_counselor(request, counselor_id):
    user = request.user
    counselor = get_object_or_404(Counselor, id=counselor_id)
    user.counselor = counselor
    user.save()
    messages.success(request, f'{counselor.username}さんがあなたのカウンセラーに選ばれました。')
    return (redirect('boards:list_themes'))

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def deselect_counselor(request):
    if request.method == 'POST':  # POSTメソッドをチェックする
        user = request.user
        user.counselor = None
        user.save()
        return redirect('accounts:home')  # リダイレクト先のURLが正しいか確認
    return redirect('accounts:home')  # GETリクエストの場合のリダイレクト先を指定

# @login_required #記載内容のバックアップです！
# def deselect_counselor(request):
#     if request.method == 'POST':
#         user = request.user
#         user.counselor = None
#         user.save()
#         return redirect('accounts:home')

# @login_required　#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
# def counselor_list(request):
#     user = request.user
#     counselors = Counselors.objects.all()

#     context = {
#         'counselors': counselors,
#         'current_user_email': user.email,  # ログインユーザーのメールアドレスをコンテキストに追加
#     }
#     return render(request, 'boards/counselor_list.html', context)

# @login_required
# def counselor_list(request):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     # ログインしているユーザーが契約しているカウンセラーを取得する例（具体的なモデルとフィールド名は適宜修正してください）
#     counselors = Counselors.objects.filter(user=request.user)
#     return render(request, 'boards/counselor_list.html', {'counselors': counselors})

# def counselor_list(request):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     counselors = Counselors.objects.all()
#     return render(request, 'boards/counselor_list.html', {'counselors': counselors})

# def edit_comment(request, comment_id):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     comment = get_object_or_404(Comments, id=comment_id)
#     # Ensure only the owner of the comment can edit it
#     if comment.user.id != request.user.id:
#         raise Http404
#     edit_comment_form = PostCommentForm(request.POST or None, instance=comment)
#     if edit_comment_form.is_valid():
#         edit_comment_form.save()
#         messages.success(request, 'コメントを更新しました。')
#         return redirect('boards:post_comments', theme_id=comment.theme.id)  # Assuming redirect to a relevant view
#     return render(
#         request, 'boards/edit_comment.html', context={
#             'edit_comment_form': edit_comment_form,
#             'id': id,
#         }
#     )

@login_required #修正完了です！
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Ensure only the owner of the comment can edit it
    if isinstance(request.user, Counselor):
        user = Users.objects.get(counselor=request.user)
        if comment.user.id != user.id:  # type: ignore
            raise Http404
    elif comment.user.id != request.user.id:
        raise Http404

    edit_comment_form = PostCommentForm(request.POST or None, instance=comment)
    if edit_comment_form.is_valid():
        edit_comment_form.save()
        messages.success(request, 'コメントを更新しました。')
        return redirect('boards:post_comments', theme_id=comment.theme.id)

    return render(
        request, 'boards/edit_comment.html', context={
            'edit_comment_form': edit_comment_form,
            'id': comment.id,  # 修正点: 'id' ではなく 'comment.id' を使用 # type: ignore
        }
    )


# def create_theme(request):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#         create_theme_form = forms.CreateThemeForm(request.POST or None) # type: ignore
#         if create_theme_form.is_valid():
#             create_theme_form.instance.user = request.user
#             create_theme_form.save()
#             messages.success(request, 'チャット画面を作成しました。')
#             return redirect('boards:list_themes')
#         return render(
#         request, 'boards/create_theme.html', context={
#             'create_theme_form': create_theme_form,
#         }
#     )

@login_required #修正完了です！この記載内容に戻れば大丈夫です！
def create_theme(request):
    if request.user.is_authenticated:
        if isinstance(request.user, Users):
            user_type = 'User'
            if request.method == 'POST':
                create_theme_form = forms.CreateThemeForm(request.POST or None)
                if create_theme_form.is_valid():
                    create_theme_form.instance.user = request.user
                    create_theme_form.save()
                    messages.success(request, 'チャット画面を作成しました。')
                    return redirect('boards:list_themes')
            else:
                create_theme_form = forms.CreateThemeForm()
            return render(request, 'boards/create_theme.html', context={
                'create_theme_form': create_theme_form,
                'user_type': user_type
            })
        elif isinstance(request.user, Counselor):
            user_type = 'Counselor'
            if request.method == 'POST':
                create_theme_form = forms.CreateThemeForm(request.POST or None)
                if create_theme_form.is_valid():
                    selected_user_id = request.POST.get('selected_user')
                    if selected_user_id:
                        try:
                            user_instance = Users.objects.get(id=selected_user_id)
                            create_theme_form.instance.user = user_instance
                            create_theme_form.save()
                            messages.success(request, 'チャット画面を作成しました。')
                            return redirect('boards:list_themes')
                        except Users.DoesNotExist:
                            messages.error(request, '選択されたユーザーが存在しません。')
                    else:
                        messages.error(request, 'ユーザーを選択してください。')
            else:
                create_theme_form = forms.CreateThemeForm()
            users = Users.objects.all()  # 選択可能なユーザーを取得
            return render(request, 'boards/create_theme.html', context={
                'create_theme_form': create_theme_form,
                'user_type': user_type,
                'users': users
            })
        else:
            return redirect('accounts:home')
    else:
        return redirect('accounts:home')



# def list_themes(request):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     themes = Themes.objects.fetch_all_themes() # type: ignore
#     return render(
#         request, 'boards/list_themes.html', context={
#             'themes': themes
#         }
#     )

# def list_themes(request):#修正完了です！デプロイサイトに記載しましょう！
#     themes = Themes.objects.filter(user=request.user)  # ログインユーザーのテーマのみ取得
#     return render(
#         request, 'boards/list_themes.html', context={
#             'themes': themes
#         }
#     )

# from django.shortcuts import redirect #この記載内容に戻りましょう!
# from django.contrib.auth import get_user_model
# User = get_user_model()

# def list_themes(request): #この記載内容に戻りましょう!
#     if request.user.is_authenticated:
#         if isinstance(request.user, User):
#             themes = Themes.objects.filter(user=request.user)  # ログインユーザーのテーマのみ取得
#             if hasattr(request.user, 'counselor'):
#                 user_type = 'Counselor'
#             else:
#                 user_type = 'User'  # デフォルトはユーザーとして設定
#         else:
#             return redirect('accounts:home')
#     else:
#         return redirect('accounts:home')

#     return render(request, 'boards/list_themes.html', {
#         'themes': themes,
#         'user_type': user_type,
#     })

@login_required #ユーザー側がログインしてしても利用可能です！カウンセラー側がログインしても利用できます！ この記載内容に戻りましょう!
def list_themes(request):
    if request.user.is_authenticated:
        if isinstance(request.user, Users):
            user_type = 'User'
            user_instance = request.user
            themes = Themes.objects.filter(user=user_instance)
            return render(request, 'boards/list_themes.html', {'themes': themes, 'user_type': user_type})
        elif isinstance(request.user, Counselor):
            user_type = 'Counselor'
            # カウンセラーが担当しているクライアントを取得する
            clients = request.user.clients.all()  # type: ignore # Adjust according to actual related name
            themes = Themes.objects.filter(user__in=clients)
            return render(request, 'boards/list_themes.html', {'themes': themes, 'user_type': user_type})
        else:
            # その他の場合はリダイレクト
            return redirect('accounts:home')
    else:
        # ログインしていない場合はログインページにリダイレクト
        return redirect('accounts:home')

# def list_themes(request): #記載内容のバックアップです!
#     if request.user.is_authenticated:
#         themes = Themes.objects.filter(user=request.user)  # ログインユーザーのテーマのみ取得

#     # もしカウンセラーでログインしている場合は、そのタイプを設定
#         if hasattr(request.user, 'counselor'):
#             user_type = 'Counselor'
#         else:
#             user_type = 'User'  # デフォルトはユーザーとして設定
#     else:
#         return redirect('accounts:home')

#     return render(request, 'boards/list_themes.html', {
#         'themes': themes,
#         'user_type': user_type,
#     })

# def edit_theme(request, id):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     theme = get_object_or_404(Themes, id=id)
#     if theme.user.id != request.user.id:
#         raise Http404
#     edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme) # type: ignore
#     if edit_theme_form.is_valid():
#         edit_theme_form.save()
#         messages.success(request, 'チャット画面を更新しました。')
#         return redirect('boards:list_themes')
#     return render(
#         request, 'boards/edit_theme.html', context={
#             'edit_theme_form': edit_theme_form,
#             'id': id,
#         }
#     )

from .forms import CreateThemeForm

@login_required #修正完了です！
def edit_theme(request, id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Themes, id=id)

        if theme.user != request.user:
            if not (isinstance(request.user, Counselor) and theme.user in request.user.clients.all()): # type: ignore
                raise Http404

        if isinstance(request.user, Users):
            user_type = 'User'
        elif isinstance(request.user, Counselor):
            user_type = 'Counselor'
        else:
            return redirect('accounts:home')

        if request.method == 'POST':
            edit_theme_form = CreateThemeForm(request.POST, instance=theme)
            if edit_theme_form.is_valid():
                edit_theme_form.save()
                messages.success(request, 'チャット画面を更新しました。')
                return redirect('boards:list_themes')
        else:
            edit_theme_form = CreateThemeForm(instance=theme)

        return render(request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'user_type': user_type,
            'id': id,
        })
    else:
        return redirect('accounts:home')


@login_required #修正完了です！
def delete_theme(request, id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Themes, id=id)

        if isinstance(request.user, Users):
            user_type = 'User'
            if theme.user == request.user:
                if request.method == 'POST':
                    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
                    if delete_theme_form.is_valid():
                        theme.delete()
                        messages.success(request, 'テーマが削除されました。')
                        return redirect('boards:list_themes')
                else:
                    delete_theme_form = forms.DeleteThemeForm()
                return render(request, 'boards/delete_theme.html', context={
                    'delete_theme_form': delete_theme_form,
                    'user_type': user_type
                })
            else:
                messages.error(request, 'このテーマを削除する権限がありません。')
                return redirect('boards:list_themes')

        elif isinstance(request.user, Counselor):
            user_type = 'Counselor'
            if theme.user in request.user.clients.all(): # type: ignore
                if request.method == 'POST':
                    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
                    if delete_theme_form.is_valid():
                        theme.delete()
                        messages.success(request, 'テーマが削除されました。')
                        return redirect('boards:list_themes')
                else:
                    delete_theme_form = forms.DeleteThemeForm()
                return render(request, 'boards/delete_theme.html', context={
                    'delete_theme_form': delete_theme_form,
                    'user_type': user_type
                })
            else:
                messages.error(request, 'このテーマを削除する権限がありません。')
                return redirect('boards:list_themes')

        else:
            return redirect('accounts:home')
    else:
        return redirect('accounts:home')

# def post_comments(request, theme_id): #記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
#     post_comment_form = forms.PostCommentForm(request.POST or None, initial={'comment': saved_comment})     # type: ignore
#     theme = get_object_or_404(Themes, id=theme_id)
#     comments = Comments.objects.fetch_by_theme_id(theme_id) # type: ignore
#     if post_comment_form.is_valid():
#         if not request.user.is_authenticated:
#             raise Http404
#         post_comment_form.instance.theme = theme
#         post_comment_form.instance.user = request.user
#         post_comment_form.save()
#         cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
#         return redirect('boards:post_comments', theme_id= theme_id)
#     return render(
#         request, 'boards/post_comments.html', context={
#             'post_comment_form': post_comment_form,
#             'theme': theme,
#             'comments': comments,
#         }
#     )

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import Http404
# from django.core.cache import cache
# from django.contrib import messages
# from .models import Themes, Comments
# from .forms import PostCommentForm

# @login_required #ユーザー側がログインした場合はコメントを入力出来ております！　問題や不具合が発生した場合この記載内容に戻りましょう！
# def post_comments(request, theme_id):
#     saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
#     post_comment_form = PostCommentForm(request.POST or None, initial={'comment': saved_comment})
#     theme = get_object_or_404(Themes, id=theme_id)
#     comments = Comments.objects.filter(theme_id=theme_id)

#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             raise Http404

#         # Save the comment
#         comment = post_comment_form.save(commit=False)
#         comment.theme = theme

#         # Set user or counselor based on the logged-in user
#         if hasattr(request.user, 'counselor'):  # Counselor instance
#             comment.counselor = request.user.counselor
#             comment.user = request.user  # カウンセラーでもuserにカウンセラーのインスタンスをセット
#         else:  # User instance
#             comment.user = request.user
#             comment.counselor = None

#         comment.save()

#         # Clear the saved comment from cache
#         cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')

#         # Redirect back to the post comments view
#         messages.success(request, 'コメントが投稿されました。')
#         return redirect('boards:post_comments', theme_id=theme.id) # type: ignore

#     return render(
#         request, 'boards/post_comments.html', context={
#             'post_comment_form': post_comment_form,
#             'theme': theme,
#             'comments': comments,
#         }
#     )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.cache import cache
from django.contrib import messages
from .models import Themes, Comments
from .forms import PostCommentForm
from accounts.models import Users, Counselor
from django.utils.functional import SimpleLazyObject

@login_required
def post_comments(request, theme_id):
    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
    post_comment_form = PostCommentForm(request.POST or None, initial={'comment': saved_comment})
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.filter(theme_id=theme_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise Http404

        # Save the comment
        comment = post_comment_form.save(commit=False)
        comment.theme = theme

        # Set user or counselor based on the logged-in user
        if isinstance(request.user._wrapped, Counselor):
            # Get the associated user for the counselor
            user = Users.objects.get(counselor=request.user)
            comment.user = user
            comment.counselor = request.user
        else:  # User instance
            comment.user = request.user
            comment.counselor = None

        comment.save()

        # Clear the saved comment from cache
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')

        # Redirect back to the post comments view
        messages.success(request, 'コメントが投稿されました。')
        return redirect('boards:post_comments', theme_id=theme.id) # type: ignore

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

def counselor_profile(request):
    counselors = Counselors.objects.all()
    return render(request, 'boards/counselor_profile.html', {'counselors': counselors})

# def delete_comment(request, comment_id):#記載内容のバックアップです！　この記載内容にもどれば大丈夫です！
#     comment = get_object_or_404(Comments, id=comment_id)
#     if request.user != comment.user:
#         raise Http404
#     if request.method == 'POST':
#         theme_id = comment.theme.id
#         theme = get_object_or_404(Themes, id=theme_id)  # テーマが存在するか確認
#         comment.delete()
#         messages.success(request, 'コメントを削除しました。')
#         return redirect('boards:post_comments', theme_id=theme_id)
#     return render(request, 'boards/delete_comment.html', context={'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Ensure only the owner of the comment can delete it
    if isinstance(request.user, Counselor):
        user = Users.objects.get(counselor=request.user)
        if comment.user.id != user.id:  # type: ignore
            raise Http404
    elif comment.user.id != request.user.id:
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
