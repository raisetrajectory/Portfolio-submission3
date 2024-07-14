from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Users
from .models import Counselor

@login_required
def counselor_profile(request):
    user_lists = []
    counselor_lists = []

    if isinstance(request.user, Users):
        user_lists = Users.objects.filter(id=request.user.id) # type: ignore
    else:
        counselor_lists = Counselor.objects.filter(id=request.user.id)

    return render(request, 'accounts/counselor_profile.html', {
        'user_lists':user_lists, 'counselor_lists':counselor_lists,
    'user': request.user})

@login_required
def counselor_menu(request):

    if isinstance(request.user, Users):
        user_type = 'User'
    else:
        user_type = 'Counselor'

    return render(request, 'base.html', {
        'user_type': user_type})

def home(request):
    return render(
        request, 'accounts/home.html'
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('accounts:home')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )

def counselor_regist(request):
    counselor_regist_form = forms.CounselorRegistForm(request.POST or None)

    if request.method == 'POST':
        if counselor_regist_form.is_valid():
            try:
                counselor_regist_form.save()
                return redirect('accounts:home')
            except ValidationError as e:
                counselor_regist_form.add_error('password', e)

    return render(
        request, 'accounts/counselor_regist.html', context={
            'counselor_regist_form': counselor_regist_form,
        }
    )

def activate_user(request, token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token) # type: ignore
    return render(
        request, 'accounts/activate_user.html'
    )

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました。')
                return redirect('accounts:home')
            else:
                messages.warning(request, 'ユーザがアクティブでありません')
        else:
            messages.warning(request, 'ユーザがパスワードが間違っています' )
    return render(
        request, 'accounts/user_login.html', context={
            'login_form':login_form,
        }
    )

def counselor_login(request): #記載内容のバックアップです!
    counselor_login_form = forms.CounselorLoginForm(request.POST or None)
    if request.method == 'POST':

        if counselor_login_form.is_valid():
            email = counselor_login_form.cleaned_data.get('email')
            password = counselor_login_form.cleaned_data.get('password')
            counselor = authenticate(request, email=email, password=password)
            if counselor:
                if counselor.is_active:
                    login(request, counselor)
                    messages.success(request, 'ログイン完了しました。')
                    return redirect('accounts:home')
                else:
                    messages.warning(request, 'カウンセラーがアクティブでありません')
            else:
                messages.warning(request, 'カウンセラーのメールアドレスまたはパスワードが間違っています')

    return render(
        request, 'accounts/counselor_login.html', context={
            'counselor_login_form': counselor_login_form,
        }
    )

# @login_required # type: ignore #記載内容のバックアップです。
# def user_logout(request):
#     logout(request)
#     messages.success(request, 'ログアウトしました')
#     return redirect('accounts:home')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:user_login')

@login_required
def counselor_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:counselor_login')

@login_required # type: ignore
def user_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if user_edit_form.is_valid():
        messages.success(request, '更新完了しました。')
        user_edit_form.save()
    return render(request, 'accounts/user_edit.html', context={
        'user_edit_form': user_edit_form,
    })

@login_required  # type: ignore #この記載内容に戻りましょう!
def counselor_edit(request):
    counselor_edit_form = forms.CounselorEditForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST':
        if counselor_edit_form.is_valid():
            counselor_edit_form.save()
            messages.success(request, '更新完了しました。')
            return redirect('accounts:counselor_edit')

    return render(request, 'accounts/counselor_edit.html', context={
        'counselor_edit_form': counselor_edit_form,
    })

# @login_required  # type: ignore
# def counselor_edit(request):
#     counselor_instance = request.user.counselor  # カウンセラーのインスタンスを取得する
#     counselor_edit_form = forms.CounselorEditForm(request.POST or None, request.FILES or None, instance=request.user.counselor)

#     if request.method == 'POST':
#         counselor_edit_form = forms.CounselorEditForm(request.POST, request.FILES, instance=counselor_instance, is_counselor=True)
#         if counselor_edit_form.is_valid():
#             counselor_edit_form.save()
#             messages.success(request, '更新完了しました。')
#             return redirect('accounts:counselor_edit')

#     return render(request, 'accounts/counselor_edit.html', context={
#         'counselor_edit_form': counselor_edit_form,
#     })

# @login_required
# def counselor_edit(request):
#     if request.user.is_authenticated and hasattr(request.user, 'counselor'):
#         counselor_instance = request.user.counselor
#     else:
#         counselor_instance = None

#     counselor_edit_form = forms.CounselorEditForm(request.POST or None, request.FILES or None, instance=counselor_instance)

#     if request.method == 'POST':
#         counselor_edit_form = forms.CounselorEditForm(request.POST, request.FILES, instance=counselor_instance)
#         if counselor_edit_form.is_valid():
#             counselor_edit_form.save()
#             messages.success(request, '更新完了しました。')
#             return redirect('accounts:counselor_edit')

#     return render(request, 'accounts/counselor_edit.html', context={
#         'counselor_edit_form': counselor_edit_form,
#     })

# @login_required  # ユーザーがログインしているか確認
# def counselor_edit(request):
#     counselor_instance = None

#     # ユーザーがログインしていて、かつCounselorオブジェクトを持っている場合にインスタンスを取得
#     if request.user.is_authenticated and hasattr(request.user, 'counselor'):
#         counselor_instance = request.user.counselor

#     # フォームをインスタンス化
#     counselor_edit_form = forms.CounselorEditForm(request.POST or None, request.FILES or None, instance=counselor_instance)

#     if request.method == 'POST':
#         # POSTメソッドで送信されたフォームをバリデーション
#         counselor_edit_form = forms.CounselorEditForm(request.POST, request.FILES, instance=counselor_instance)
#         if counselor_edit_form.is_valid():
#             counselor_edit_form.save()  # フォームがバリデーションを通過したら保存
#             messages.success(request, '更新完了しました。')  # 成功メッセージを表示
#             return redirect('accounts:counselor_edit')  # リダイレクト

#     return render(request, 'accounts/counselor_edit.html', context={
#         'counselor_edit_form': counselor_edit_form,  # フォームをコンテキストに渡す
#     })


# @login_required
# def counselor_edit(request):
#     counselor_instance = Counselor.objects.get(user=request.user)  # ログイン中のユーザーに対応するカウンセラーインスタンスを取得します
#     counselor_edit_form = forms.CounselorEditForm(request.POST or None, instance=counselor_instance, is_counselor=True)

#     if request.method == 'POST':
#         if counselor_edit_form.is_valid():
#             counselor_edit_form.save()
#             messages.success(request, '更新完了しました。')
#             return redirect('accounts:counselor_edit')

#     return render(request, 'accounts/counselor_edit.html', context={
#         'counselor_edit_form': counselor_edit_form,
#     })


@login_required  # type: ignore
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワード更新完了しました。')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(
        request, 'accounts/change_password.html', context={
            'password_change_form': password_change_form,
        }
    )


def show_error_page(request, exception):
    return render(
        request, '404.html'
    )

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import CounselorEditForm
# from .models import Counselor

# def edit_counselor(request):
#     counselor_instance = Counselor.objects.get(user=request.user)  # ログイン中のユーザーに対応するカウンセラーインスタンスを取得します
#     if request.method == 'POST':
#         form = CounselorEditForm(request.POST, request.FILES, instance=counselor_instance, is_counselor=True)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'カウンセラー情報が更新されました！')
#             return redirect('some_redirect_view')  # 更新後のリダイレクト先を指定します
#     else:
#         form = CounselorEditForm(instance=counselor_instance, is_counselor=True)

#     context = {
#         'form': form,
#     }
#     return render(request, 'edit_counselor.html', context)

