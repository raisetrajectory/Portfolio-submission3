from django.shortcuts import render, redirect
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from .models import Users
from .models import Counselor

@login_required #記載内容のバックアップです! この記載内容に戻りましょう!
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

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Users, Counselor

# @login_required
# def counselor_profile(request):
#     user_lists = []
#     counselor_lists = []

#     if hasattr(request.user, 'is_counselor') and request.user.is_counselor:  # カウンセラーがログインしている場合
#         counselor = request.user
#         user_lists = Users.objects.filter(counselor=counselor)  # ログインしているカウンセラーに関連するユーザーを取得
#         counselor_lists = [counselor]
#     else:  # ユーザーがログインしている場合
#         user = request.user
#         counselor = user.counselor if hasattr(user, 'counselor') else None
#         if counselor:
#             user_lists = [user]  # 契約しているユーザーの情報を表示
#             counselor_lists = [counselor]  # 契約しているカウンセラーの情報を表示
#         else:
#             user_lists = [user]  # カウンセラーがない場合は、ユーザー自身の情報を表示
#             counselor_lists = []

#     return render(request, 'accounts/counselor_profile.html', {
#         'user_lists': user_lists,
#         'counselor_lists': counselor_lists,
#         'user': request.user
#     })


@login_required #記載内容のバックアップです! この記載内容に戻りましょう!
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

