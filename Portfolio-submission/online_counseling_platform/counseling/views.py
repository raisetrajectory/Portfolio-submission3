# # counseling/views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, logout, authenticate  # authenticateを追加
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.template.loader import get_template
# from django.template import TemplateDoesNotExist
# from django.contrib.auth import views as auth_views
# from .forms import CustomUserCreationForm, CustomAuthenticationForm, CounselorForm, ProfileForm, ChatMessageForm  # すべてのフォームを一行でインポート
# from .models import Counselor, CounselingSession, ChatMessage

# def home(request):
#     return render(request, 'home.html')

# @login_required
# def session_detail(request, session_id):
#     session = get_object_or_404(CounselingSession, id=session_id)
#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
#     return render(request, 'session_detail.html', {'session': session, 'messages': messages})

# # def chat_view(request):
# #     messages = ChatMessage.objects.all()
# #     try:
# #         template = get_template('counseling/registration/chat.html')
# #     except TemplateDoesNotExist:
# #         raise TemplateDoesNotExist("The template 'counseling/registration/chat.html' does not exist.")
# #     return render(request, 'counseling/registration/chat.html', {'messages': messages})

# @login_required
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = request.user
#             chat_message.session = session
#             chat_message.save()
#             return redirect('chat_view', session_id=session.id) # type: ignore
#     else:
#         form = ChatMessageForm()
#     messages = ChatMessage.objects.filter(session=session).order_by('-timestamp') if session else []
#     return render(request, 'counseling/registration/chat.html', {'form': form, 'messages': messages, 'session': session})

# @login_required
# def create_session(request):
#     if request.method == 'POST':
#         counselor_id = request.POST.get('counselor')
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session = CounselingSession.objects.create(user=request.user, counselor=counselor)
#         return redirect('chat_view', counselor_id=counselor.id) # type: ignore

#     counselors = Counselor.objects.all()
#     return render(request, 'create_session.html', {'counselors': counselors})

# def counselor_profile(request, pk):
#     counselor = get_object_or_404(Counselor, pk=pk)
#     return render(request, 'counselor_profile.html', {'counselor': counselor})

# def edit_counselor_profile(request, pk):
#     counselor = get_object_or_404(Counselor, pk=pk)
#     if request.method == 'POST':
#         form = CounselorForm(request.POST, instance=counselor)
#         if form.is_valid():
#             form.save()
#             return redirect('counselor_profile', pk=counselor.pk)
#     else:
#         form = CounselorForm(instance=counselor)
#     return render(request, 'edit_counselor_profile.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# def login_view(request):
#     return auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm)(request)

# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('home')
#     return render(request, 'logout.html')

# @login_required
# def profile_view(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user)
#     return render(request, 'profile.html', {'form': form})

# def counselor_list_view(request):
#     counselors = Counselor.objects.all()
#     return render(request, 'counselor_list.html', {'counselors': counselors})

# def get_messages(request):
#     messages = ChatMessage.objects.values('user', 'content')
#     return JsonResponse({'messages': list(messages)})

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = request.user
#             session_id = request.POST.get('session_id')
#             if session_id:
#                 chat_message.session = get_object_or_404(CounselingSession, id=session_id)
#             chat_message.save()
#             if session_id:  # session_id が存在する場合のみリダイレクト
#                 return redirect('chat_view', session_id=session_id)
#     return redirect('home')  # フォームが無効な場合やPOST以外のリクエストの場合はホームにリダイレクト

# 1~130の記載内容に関しては、現段階で問題無い記載となっております。バックアップ保存用です！

# counseling/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CounselorForm, ProfileForm, ChatMessageForm
from .models import Counselor, CounselingSession, ChatMessage
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from django.urls import reverse
from django.contrib import messages

import os #2024年6月5日追加
from django.core.files.storage import FileSystemStorage #2024年6月5日追加
from django.http import HttpResponseRedirect #2024年6月5日追加
from .forms import UploadFileForm #2024年6月6日追加
from django.conf import settings #2024年6月6日追加

User = get_user_model()

from django.views.decorators.csrf import csrf_exempt

# from .models import Profile #2024年6月6日追加

# def profile(request): #2024年6月6日追加
#     if request.method == 'POST' and request.FILES.get('upload_file'):
#         upload_file = request.FILES['upload_file']
#         fs = FileSystemStorage()
#         file_path = fs.save(upload_file.name, upload_file)
#         uploaded_file_url = fs.url(file_path)
#         request.session['uploaded_file_url'] = uploaded_file_url  # セッションに保存
#         print("uploaded_file_url:", uploaded_file_url)  # ログに出力
#         return redirect('profile')
#     return render(request, 'profile.html')

def profile(request): #2024年6月6日追加
    if request.method == 'POST' and request.FILES['upload_file']:
        uploaded_file = request.FILES['upload_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        request.session['uploaded_file_url'] = uploaded_file_url
    return render(request, 'profile.html', {'user': request.user})

# def profile(request):
#     if request.method == 'POST' and request.FILES['upload_file']:
#         uploaded_file = request.FILES['upload_file']
#         profile = Profile(user=request.user, profile_picture=uploaded_file)
#         profile.save()
#     return render(request, 'profile.html', {'user': request.user})

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

# def upload_sample(request): #2024年6月6日追加
#     if request.method == 'POST' and request.FILES['upload_file']:
#         upload_file = request.FILES['upload_file']
#         fs = FileSystemStorage(location=settings.MEDIA_ROOT)
#         file_path = fs.save(upload_file.name, upload_file)
#         uploaded_file_url = fs.url(file_path)
#         request.session['uploaded_file_url'] = uploaded_file_url  # セッションに保存
#         return HttpResponseRedirect(reverse('profile'))
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

def home(request):
    some_condition = not User.objects.filter(username='default_user').exists()
    if some_condition:
        User.objects.create_user(username='default_user', password='defaultpassword')
    return render(request, 'home.html')

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(CounselingSession, id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'session_detail.html', {'session': session, 'messages': messages})

#193~210の記載内容が正しいです！バックアップです！
# @login_required
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     form = ChatMessageForm(initial={'session_id': session.id}) if session else ChatMessageForm()
#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

#     return render(request, 'counseling/registration/chat.html', {
#         'form': form,
#         'messages': messages,
#         'session': session,
#         'user': request.user,
#     })

# @login_required #2024年6月9日追加
# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = request.user
#             chat_message.session = get_object_or_404(CounselingSession, id=form.cleaned_data['session_id'])
#             chat_message.save()
#             # メッセージを保存した後に直接チャット画面を表示する
#             return redirect('chat_view', session_id=form.cleaned_data['session_id'])
#     return redirect('chat_view') #コメントを入力後にチャット画面にリダイレクト出来ております！

# @login_required #2024年6月11日追加 この記載内容に戻りましょう！
# def send_message(request):
#     if request.method == 'POST':
#         session_id = request.POST.get('session_id')
#         form = ChatMessageForm(request.POST, session_id=session_id)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = request.user
#             chat_message.session_id = session_id
#             chat_message.save()
#             # コメントを入力して画面に表示させる処理
#             data = {
#                 'sender': chat_message.sender.username,
#                 'message': chat_message.message,
#                 'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#                 'success': True,
#             }
#             return JsonResponse(data)
#         else:
#             errors = form.errors.get_json_data()
#             return JsonResponse({'success': False, 'errors': errors})
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        form = ChatMessageForm(request.POST, session_id=session_id)
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

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    session_id = message.session.id
    if request.user == message.sender:
        message.delete()
    return redirect('chat_view', session_id=session_id)

# @login_required #2024年6月9日追加 記載内容のバックアップです！ ここに戻りましょう！
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
#             chat_message = form.save(commit=False)
#             chat_message.sender = request.user
#             chat_message.session = session
#             chat_message.save()
#             return redirect('chat_view', session_id=session.id)

#     print(messages)  # メッセージの内容を出力

#     form = ChatMessageForm(initial={'session_id': session.id}) if session else ChatMessageForm()
#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

#     return render(request, 'counseling/registration/chat.html', {
#         'form': form,
#         'messages': messages,
#         'session': session,
#         'user': request.user,
#     })

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

# @login_required
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, _ = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST, session_id=session.id if session else None)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.session = session
#             message.save()
#             return redirect('chat_view', session_id=session.id if session else None)
#         else:
#             print(form.errors)
#     else:
#         form = ChatMessageForm(session_id=session.id if session else None)

#     messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

#     return render(request, 'counseling/registration/chat.html', {
#         'form': form,
#         'messages': messages,
#         'session': session,
#         'user': request.user,
#     })

@login_required
def chat_view(request, session_id=None, counselor_id=None):
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
            message.save()
            return redirect('chat_view', session_id=session.id if session else None)
        else:
            print(form.errors)
    else:
        initial = {'session_id': session.id} if session else {}
        form = ChatMessageForm(initial=initial)

    messages = ChatMessage.objects.filter(session=session).order_by('timestamp') if session else []

    return render(request, 'counseling/registration/chat.html', {
        'form': form,
        'messages': messages,
        'session': session,
        'user': request.user,
    })

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# @login_required #2024年6月4日追加
# def profile_view(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profile.html', {'form': form})

def counselor_list_view(request):
    counselors = Counselor.objects.all()
    return render(request, 'counselor_list.html', {'counselors': counselors})
