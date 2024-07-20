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
from django.http import Http404
from django.contrib import messages
from .models import Comments
from .forms import PostCommentForm
from django.shortcuts import render
from .models import Counselors
from accounts.models import Counselor, Users
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Themes
from .forms import CreateThemeForm
from django.core.cache import cache
from .models import Themes, Comments
from accounts.models import Users, Counselor
from django.utils.functional import SimpleLazyObject
from django.shortcuts import redirect
from .models import Counselor

@login_required
def theme_list(request):
    # ログインしているユーザーが作成していないテーマを取得
    themes = Themes.objects.exclude(user=request.user)
    # ログインしているユーザーが作成したテーマを取得
    themes = Themes.objects.filter(user=request.user)
    return render(request, 'boards/list_themes.html', {
        'themes': themes,
    })

# @login_required
# def theme_list(request):
#     user = request.user

#     if user.is_counselor:
#         # カウンセラーの場合、契約しているユーザーが作成したテーマのみを取得
#         if user.counselor:
#             # 契約している利用者を取得
#             users = Users.objects.filter(counselor=user.counselor)
#             themes = Themes.objects.filter(user__in=users)
#         else:
#             # 契約している利用者がいない場合は空のテーマリスト
#             themes = Themes.objects.none()
#     else:
#         # 一般のユーザーの場合、自分が作成したテーマのみを取得
#         themes = Themes.objects.filter(user=user)

#     return render(request, 'boards/list_themes.html', {
#         'themes': themes,
#     })

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

# @login_required #記載内容のバックアップです！ この記載内容戻りましょう!
# def select_counselor(request, counselor_id):
#     user = request.user
#     counselor = get_object_or_404(Counselor, id=counselor_id)
#     user.counselor = counselor
#     user.save()
#     messages.success(request, f'{counselor.username}さんがあなたのカウンセラーに選ばれました。')
#     return (redirect('boards:list_themes'))

@login_required #既に他のカウンセラーと契約中です。契約を解除してから新しいカウンセラーを選択してください。と表示されます！
def select_counselor(request, counselor_id):
    user = request.user
    counselor = get_object_or_404(Counselor, id=counselor_id)

    # ユーザーが既に契約中のカウンセラーがいる場合は契約を許可しない
    if user.counselor:
        messages.error(request, '既に他のカウンセラーと契約中です。契約を解除してから新しいカウンセラーを選択してください。')
        return redirect('boards:counselor_list')

    user.counselor = counselor
    user.save()
    messages.success(request, f'{counselor.username}さんがあなたのカウンセラーに選ばれました。')
    return redirect('boards:list_themes')


# @login_required
# def select_counselor(request, counselor_id):
#     user = request.user
#     counselor = get_object_or_404(Counselor, id=counselor_id)
#     user.counselor = counselor
#     user.save()
#     messages.success(request, f'{counselor.username}さんがあなたのカウンセラーに選ばれました。')
#     return redirect('boards:list_themes', counselor_id=counselor.id) # type: ignore


# @login_required #記載内容のバックアップです！
# def deselect_counselor(request):
#     if request.method == 'POST':  # POSTメソッドをチェックする
#         user = request.user
#         user.counselor = None
#         user.save()
#         return redirect('accounts:home')  # リダイレクト先のURLが正しいか確認
#     return redirect('accounts:home')  # GETリクエストの場合のリダイレクト先を指定

# @login_required #記載内容のバックアップです！ この記載内容戻りましょう!
# def deselect_counselor(request, counselor_id):
#     counselor = get_object_or_404(Counselor, id=counselor_id)
#     if request.method == 'POST':
#         request.user.counselor = None
#         request.user.save()
#         return redirect('boards:counselor_list')
#     return render(request, 'boards/counselor_list.html', {'counselors': Counselor.objects.all()})

@login_required
def deselect_counselor(request, counselor_id):
    user = request.user
    counselor = get_object_or_404(Counselor, id=counselor_id)

    # ユーザーが現在契約中のカウンセラーであることを確認
    if user.counselor != counselor:
        messages.error(request, 'このカウンセラーとは契約していません。')
        return redirect('boards:counselor_list')

    if request.method == 'POST':
        user.counselor = None
        user.save()
        messages.success(request, f'{counselor.username}さんとの契約を解除しました。')
        return redirect('boards:counselor_list')

    return render(request, 'boards/counselor_list.html', {'counselors': Counselor.objects.all()})


@login_required#ユーザー側がログインしてしても利用可能です！カウンセラー側がログインしても利用できます！ この記載内容に戻りましょう!
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Ensure only the owner of the comment or a counselor can edit it
    if request.user.is_authenticated:
        if isinstance(request.user, Counselor):
            # Check if the counselor is associated with a user
            try:
                user = Users.objects.get(counselor=request.user)
            except Users.DoesNotExist:
                user = None

            if comment.counselor != request.user and comment.user != user:
                raise Http404
        elif comment.user != request.user:
            raise Http404
    else:
        raise Http404

    edit_comment_form = PostCommentForm(request.POST or None, instance=comment)
    if edit_comment_form.is_valid():
        edit_comment_form.save()
        messages.success(request, 'コメントを更新しました。')
        return redirect('boards:post_comments', theme_id=comment.theme.id)

    return render(
        request, 'boards/edit_comment.html', context={
            'edit_comment_form': edit_comment_form,
            'comment': comment,
        }
    )

@login_required
def create_theme(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            create_theme_form = CreateThemeForm(request.POST)
            if create_theme_form.is_valid():
                theme = create_theme_form.save(commit=False)
                if isinstance(request.user, Counselor):
                    selected_user_id = request.POST.get('selected_user')
                    if selected_user_id:
                        try:
                            user_instance = Users.objects.get(id=selected_user_id)
                            theme.user = user_instance
                        except Users.DoesNotExist:
                            messages.error(request, '選択されたユーザーが存在しません。')
                            return render(request, 'boards/create_theme.html', {
                                'create_theme_form': create_theme_form,
                                'user_type': 'Counselor',
                                'users': Users.objects.all()
                            })
                    else:
                        messages.error(request, 'ユーザーを選択してください。')
                        return render(request, 'boards/create_theme.html', {
                            'create_theme_form': create_theme_form,
                            'user_type': 'Counselor',
                            'users': Users.objects.all()
                        })
                else:
                    theme.user = request.user
                theme.save()
                messages.success(request, 'チャット画面を作成しました。')
                return redirect('boards:list_themes')  # チャット一覧画面へのリダイレクト
        else:
            create_theme_form = CreateThemeForm()

        if isinstance(request.user, Counselor):
            user_type = 'Counselor'
            users = Users.objects.all()  # 選択可能なユーザーを取得
        else:
            user_type = 'User'
            users = None  # ユーザー側でのフォームでは選択肢を表示しない

        return render(request, 'boards/create_theme.html', {
            'create_theme_form': create_theme_form,
            'user_type': user_type,
            'users': users
        })
    else:
        return redirect('accounts:home')

@login_required #ユーザー側がログインしてしても利用可能です！カウンセラー側がログインしても利用できます！ この記載内容に戻りましょう!
def list_themes(request):
    if isinstance(request.user, Users):
        themes = Themes.objects.filter(user=request.user)
    elif isinstance(request.user, Counselor):
        themes = Themes.objects.filter(user__in=Users.objects.all())
    else:
        themes = Themes.objects.none()

    return render(request, 'boards/list_themes.html', {
        'themes': themes,
    })

# @login_required #修正完了です！ 記載内容のバックアップです！ この記載内容に戻りましょう！
# def edit_theme(request, id):
#     if request.user.is_authenticated:
#         theme = get_object_or_404(Themes, id=id)
#         if theme.user != request.user:
#             if not (isinstance(request.user, Counselor) and theme.user in request.user.clients.all()): # type: ignore
#                 raise Http404
#         if isinstance(request.user, Users):
#             user_type = 'User'
#         elif isinstance(request.user, Counselor):
#             user_type = 'Counselor'
#         else:
#             return redirect('accounts:home')
#         if request.method == 'POST':
#             edit_theme_form = CreateThemeForm(request.POST, instance=theme)
#             if edit_theme_form.is_valid():
#                 edit_theme_form.save()
#                 messages.success(request, 'チャット画面を更新しました。')
#                 return redirect('boards:list_themes')
#         else:
#             edit_theme_form = CreateThemeForm(instance=theme)
#         return render(request, 'boards/edit_theme.html', context={
#             'edit_theme_form': edit_theme_form,
#             'user_type': user_type,
#             'id': id,
#         })
#     else:
#         return redirect('accounts:home')

from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Themes, Users, Counselor
from .forms import CreateThemeForm

@login_required
def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)

    # ユーザーがテーマの所有者であるか、またはカウンセラーでそのクライアントであるかを確認
    is_owner = theme.user == request.user
    is_counselor = Counselor.objects.filter(id=request.user.id).exists()
    is_client = is_counselor and theme.user.counselor == request.user

    if not (is_owner or is_client):
        print(f"Page not found: is_owner={is_owner}, is_counselor={is_counselor}, is_client={is_client}")
        raise Http404

    if request.method == 'POST':
        edit_theme_form = CreateThemeForm(request.POST, instance=theme)
        if edit_theme_form.is_valid():
            edit_theme_form.save()
            messages.success(request, 'チャット画面を更新しました。')
            return redirect('boards:list_themes')
    else:
        edit_theme_form = CreateThemeForm(instance=theme)

    user_type = 'Counselor' if is_counselor else 'User'

    return render(request, 'boards/edit_theme.html', context={
        'edit_theme_form': edit_theme_form,
        'user_type': user_type,
        'id': id,
        'theme': theme,  # テーマオブジェクトをテンプレートに渡す
    })


@login_required #修正完了です！　記載内容のバックアップです！ この記載内容に戻りましょう！
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
                        messages.success(request, 'チャット画面が削除されました。')
                        return redirect('boards:list_themes')
                else:
                    delete_theme_form = forms.DeleteThemeForm()
                return render(request, 'boards/delete_theme.html', context={
                    'delete_theme_form': delete_theme_form,
                    'user_type': user_type
                })
            else:
                messages.error(request, 'このチャット画面を削除する権限がありません。')
                return redirect('boards:list_themes')
        elif isinstance(request.user, Counselor):
            user_type = 'Counselor'
            if theme.user in request.user.clients.all(): # type: ignore
                if request.method == 'POST':
                    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
                    if delete_theme_form.is_valid():
                        theme.delete()
                        messages.success(request, 'チャット画面が削除されました。')
                        return redirect('boards:list_themes')
                else:
                    delete_theme_form = forms.DeleteThemeForm()
                return render(request, 'boards/delete_theme.html', context={
                    'delete_theme_form': delete_theme_form,
                    'user_type': user_type
                })
            else:
                messages.error(request, 'このチャット画面を削除する権限がありません。')
                return redirect('boards:list_themes')
        else:
            return redirect('accounts:home')
    else:
        return redirect('accounts:home')

@login_required #ユーザー側がログインしている場合はコメント入力出来ます！ カウンセラー側がログインしている場合はコメント入力出来ます！ 問題や不具合が発生した場合はこの記載内容を戻りましょう！
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
        if isinstance(request.user, Counselor):
            comment.counselor = request.user
            comment.user = None  # Set user to None for counselors
        else:  # User instance
            comment.user = request.user
            comment.counselor = None

        comment.save()
        # Clear the saved comment from cache
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}') # type: ignore

        # Redirect back to the post comments view
        messages.success(request, 'コメントが投稿されました。')
        return redirect('boards:post_comments', theme_id=theme.id) # type: ignore

    return render(request, 'boards/post_comments.html', context={
        'post_comment_form': post_comment_form,
        'theme': theme,
        'comments': comments,
    })

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

@login_required#ユーザー側がログインしている場合はコメント削除出来ます！ カウンセラー側がログインしている場合はコメント削除出来ます！
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Ensure only the owner of the comment or a counselor can delete it
    if isinstance(request.user, Counselor):
        # Check if the counselor is associated with a user
        try:
            user = Users.objects.get(counselor=request.user)
        except Users.DoesNotExist:
            user = None

        if comment.user != user:
            raise Http404
    elif comment.user != request.user:
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
