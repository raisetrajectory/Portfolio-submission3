# counseling/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CounselorForm, ProfileForm, ChatMessageForm
from .models import Counselor, CounselingSession, ChatMessage
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.core.files.storage import FileSystemStorage #2024年6月5日追加
from django.http import HttpResponseRedirect #2024年6月5日追加
from .forms import UploadFileForm #2024年6月6日追加
from django.conf import settings #2024年6月6日追加

User = get_user_model()

from . import forms #2024年6月11日追加
from django.core.exceptions import ValidationError #2024年6月11日追加
# from .models import UserActivateTokens # type: ignore #2024年6月11日追加
from django.shortcuts import render, redirect #2024年6月11日追加
from django.contrib.auth import authenticate, login, logout #2024年6月11日追加
from django.contrib import messages #2024年6月11日追加
from django.contrib.auth.decorators import login_required #2024年6月11日追加
from django.contrib.auth import update_session_auth_hash #2024年6月11日追加

def home(request):  # type: ignore
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

def regist(request): # type: ignore #6月12日追加
    regist_form = forms.RegistForm(request.POST or None) # type: ignore
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('counseling:home2')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'counseling/regist.html', context={
            'regist_form': regist_form,
        }
    )

# def regist(request): #6月12日追加
#     regist_form = forms.RegistForm(request.POST or None) # type: ignore
#     if regist_form.is_valid():
#         try:
#             regist_form.save()
#             return redirect('counseling:home')
#         except ValidationError as e:
#             regist_form.add_error('password', e)
#     return render(
#         request, 'counseling/regist.html', context={
#             'regist_form': regist_form,
#         }
#     )

def activate_user(request, token): #6月12日追加
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token) # type: ignore
    return render(
        request, 'counseling/activate_user.html'
    )

def user_login(request): # type: ignore #6月12日追加
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました。')
                return redirect('counseling:home2')
            else:
                messages.warning(request, 'ユーザがアクティブでありません')
        else:
            messages.warning(request, 'ユーザがパスワードが間違っています' )
    return render(
        request, 'counseling/user_login.html', context={
            'login_form':login_form,
        }
    )

# def user_login(request): #6月12日追加
#     login_form = forms.LoginForm(request.POST or None)
#     if login_form.is_valid():
#         email = login_form.cleaned_data.get('email')
#         password = login_form.cleaned_data.get('password')
#         user = authenticate(email=email, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 messages.success(request, 'ログイン完了しました。')
#                 return redirect('counseling:home')
#             else:
#                 messages.warning(request, 'ユーザがアクティブでありません')
#         else:
#             messages.warning(request, 'ユーザがパスワードが間違っています' )
#     return render(
#         request, 'counseling/user_login.html', context={
#             'login_form':login_form,
#         }
#     )

@login_required #6月12日追加
def user_logout(request): # type: ignore
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('counseling:home2')

# @login_required #6月12日追加
# def user_logout(request):
#     logout(request)
#     messages.success(request, 'ログアウトしました')
#     return redirect('counseling:home')

@login_required #6月12日追加
def user_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user) # type: ignore
    if user_edit_form.is_valid():
        messages.success(request, '更新完了しました。')
        user_edit_form.save()
    return render(request, 'counseling/user_edit.html', context={
        'user_edit_form': user_edit_form,
    })

@login_required #6月12日追加
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user) # type: ignore
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワード更新完了しました。')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(
        request, 'counseling/change_password.html', context={
            'password_change_form': password_change_form,
        }
    )

def show_error_page(request, exception):
    return render(
        request, '404.html'
    )


@login_required #2024年6月11日追加　
def chat_view(request,session_id=None, counselor_id=None):
    session = None
    if session_id:
        session = get_object_or_404(CounselingSession, id=session_id)
    elif counselor_id:
        counselor = get_object_or_404(Counselor, id=counselor_id)
        session, _ = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.session = session
            message.session_id = session.id  # type: ignore # session_id を設定
            message.save()
            return redirect('chat_view', session_id=session.id) # type: ignore
        else:
            print(form.errors)
    else:
        initial = {'session_id': session.id} if session else {} # type: ignore
        form = ChatMessageForm(initial=initial)

    messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

    # デバッグ用のプリント文
    print(f'Session ID: {session.id}' if session else 'No session') # type: ignore

    return render(request, 'counseling/registration/chat.html', {
        'form': form,
        'messages': messages,
        'session': session,
        'user': request.user,
    })

# @login_required
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, _ = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.session = session
#             message.save()
#             return redirect('chat_view', session_id=session.id) # type: ignore
#         else:
#             print(form.errors)
#     else:
#         form = ChatMessageForm()

#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

#     # デバッグ用のプリント文
#     print(f'Session ID: {session.id}' if session else 'No session') # type: ignore

#     return render(request, 'counseling/registration/chat.html', {
#         'form': form,
#         'messages': messages,
#         'session': session,
#         'user': request.user,
#     })

@login_required #2024年6月11日追加です！
def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        if not session_id:
            return JsonResponse({'success': False, 'error': 'セッションIDを設定してください。'})

        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.session_id = session_id
            chat_message.save()
            data = {
                'sender': chat_message.sender.username,
                'message': chat_message.message,
                'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'success': True,
            }
            return JsonResponse(data)
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def profile(request): #2024年6月6日追加
    if request.method == 'POST' and request.FILES['upload_file']:
        uploaded_file = request.FILES['upload_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        request.session['uploaded_file_url'] = uploaded_file_url
    return render(request, 'profile.html', {'user': request.user})

def upload_sample(request): #2024年6月6日追加
    if request.method == 'POST' and request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        file_path = fs.save(upload_file.name, upload_file)
        uploaded_file_url = fs.url(file_path)
        return HttpResponseRedirect(reverse('profile') + '?uploaded_file_url=' + uploaded_file_url)
    else:
        form = UploadFileForm()
    return render(request, 'online_counseling_platform/profile.html', {'form': form})

def home(request):
    some_condition = not User.objects.filter(username='default_user').exists()
    if some_condition:
        User.objects.create_user(username='default_user', password='defaultpassword') # type: ignore
    return render(request, 'home.html')

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(CounselingSession, id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'session_detail.html', {'session': session, 'messages': messages})

@login_required
def create_session(request):
    if request.method == 'POST':
        counselor_id = request.POST.get('counselor')
        counselor = get_object_or_404(Counselor, id=counselor_id)
        session = CounselingSession.objects.create(user=request.user, counselor=counselor)
        return redirect('chat_view', counselor_id=counselor.id) # type: ignore

    counselors = Counselor.objects.all()
    return render(request, 'create_session.html', {'counselors': counselors})

def counselor_profile(request, pk):
    counselor = get_object_or_404(Counselor, pk=pk)
    return render(request, 'counselor_profile.html', {'counselor': counselor})

def edit_counselor_profile(request, pk):
    counselor = get_object_or_404(Counselor, pk=pk)
    if request.method == 'POST':
        form = CounselorForm(request.POST, instance=counselor)
        if form.is_valid():
            form.save()
            return redirect('counselor_profile', pk=counselor.pk)
    else:
        form = CounselorForm(instance=counselor)
    return render(request, 'edit_counselor_profile.html', {'form': form})

def signup(request): #2024年6月5日追加 ユーザー登録出来ております！
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ユーザーオブジェクトにbackend属性を追加
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 使用しているバックエンドを指定
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  # 適切なリダイレクト先に変更
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    return auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm)(request)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout.html')

def counselor_list_view(request):
    counselors = Counselor.objects.all()
    return render(request, 'counselor_list.html', {'counselors': counselors})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    session_id = message.session.id # type: ignore
    if request.user == message.sender:
        message.delete()
    return redirect('chat_view', session_id=session_id)

@login_required #2024年6月4日追加
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# @login_required #2024年6月11日追加 記載内容のバックアップです！ ここに戻りましょう！
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, _ = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST, initial={'session_id': session.id if session else None})
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.session = session
#             message.save()
#             # return redirect('chat_view', session_id=session.id)  # チャット画面にリダイレクト
#             return redirect('chat_view', session_id=session.id if session else None)
#         else:
#             print(form.errors)  # フォームのエラーをデバッグ出力
#     else:
#         form = ChatMessageForm(initial={'session_id': session.id if session else None})

#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

#     return render(request, 'counseling/registration/chat.html', {
#         'form': form,
#         'messages': messages,
#         'session': session,
#         'user': request.user,
#     })