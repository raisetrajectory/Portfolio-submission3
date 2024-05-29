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
from django.contrib.auth import login, logout, authenticate  # authenticateを追加
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CounselorForm, ProfileForm, ChatMessageForm  # すべてのフォームを一行でインポート
from .models import Counselor, CounselingSession, ChatMessage
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AbstractBaseUser

def home(request):
    return render(request, 'home.html')

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(CounselingSession, id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'session_detail.html', {'session': session, 'messages': messages})

# def chat_view(request):
#     messages = ChatMessage.objects.all()
#     try:
#         template = get_template('counseling/registration/chat.html')
#     except TemplateDoesNotExist:
#         raise TemplateDoesNotExist("The template 'counseling/registration/chat.html' does not exist.")
#     return render(request, 'counseling/registration/chat.html', {'messages': messages})

# @login_required
# def chat_view(request, session_id=None, counselor_id=None):
#     session = None
#     if session_id:
#         session = get_object_or_404(CounselingSession, id=session_id)
#         messages = ChatMessage.objects.filter(session=session)
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
#         messages = ChatMessage.objects.filter(session=session)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = get_user_model().objects.get(pk=request.user.pk)
#             chat_message.session = session
#             chat_message.save()
#             return redirect('chat_view', session_id=session.id)  # type: ignore
#     else:
#         form = ChatMessageForm()
#     messages = ChatMessage.objects.filter(session=session).order_by('-timestamp') if session else []
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
#         messages = ChatMessage.objects.filter(session=session)
#     elif counselor_id:
#         counselor = get_object_or_404(Counselor, id=counselor_id)
#         session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.sender = get_user_model().objects.get(pk=request.user.pk)
#             chat_message.session = session
#             chat_message.save()
#             return redirect('chat_view', session_id=session.id)  # type: ignore
#     else:
#         form = ChatMessageForm()
#     messages = ChatMessage.objects.filter(session=session).order_by('-timestamp') if session else []
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
        messages = ChatMessage.objects.filter(session=session)
    elif counselor_id:
        counselor = get_object_or_404(Counselor, id=counselor_id)
        session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user  # request.user をそのまま使用
            chat_message.session = session
            chat_message.save()
            return redirect('chat_view', session_id=session.id)  # type: ignore
    else:
        form = ChatMessageForm()
    messages = ChatMessage.objects.filter(session=session).order_by('-timestamp') if session else []
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

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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

def counselor_list_view(request):
    counselors = Counselor.objects.all()
    return render(request, 'counselor_list.html', {'counselors': counselors})

def get_messages(request):
    messages = ChatMessage.objects.values('user', 'content')
    return JsonResponse({'messages': list(messages)})

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             user = request.user
#             if isinstance(user, SimpleLazyObject):
#                 user._setup()
#                 user = user._wrapped
#             User = get_user_model()
#             if isinstance(user, User):
#                 chat_message.sender = user
#             session_id = request.POST.get('session_id')
#             if session_id:
#                 chat_message.session = get_object_or_404(CounselingSession, id=session_id)
#             chat_message.save()
#             if session_id:
#                 return redirect('chat_view', session_id=session_id)
#     return redirect('home')

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             user = request.user
#             if isinstance(user, SimpleLazyObject):
#                 user._setup()
#                 user = user._wrapped
#             User = get_user_model()
#             if isinstance(user, User):
#                 chat_message.sender = user
#             session_id = request.POST.get('session_id')
#             if session_id:
#                 chat_message.session = get_object_or_404(CounselingSession, id=session_id)
#             chat_message.save()
#             if session_id:
#                 return redirect('chat_view', session_id=session_id)
#     return redirect('home')

# @login_required
# def delete_message(request, message_id):
#     message = get_object_or_404(ChatMessage, id=message_id)
#     session_id = message.session.id
#     if request.user == message.sender:
#         message.delete()
#     return redirect('chat_view', session_id=session_id)

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             user = request.user
#             # Ensure user is not a SimpleLazyObject
#             if isinstance(user, SimpleLazyObject):
#                 user._setup()
#                 user = user._wrapped
#             User = get_user_model()
#             if isinstance(user, User):
#                 chat_message.sender = user
#             else:
#                 return redirect('home')  # Handle case where user is not valid
#             session_id = request.POST.get('session_id')
#             if session_id:
#                 chat_message.session = get_object_or_404(CounselingSession, id=session_id)
#             chat_message.save()
#             if session_id:
#                 return redirect('chat_view', session_id=session_id)
#     return redirect('home')

# @login_required
# def delete_message(request, message_id):
#     message = get_object_or_404(ChatMessage, id=message_id)
#     session_id = message.session.id
#     if request.user == message.sender:
#         message.delete()
#     return redirect('chat_view', session_id=session_id)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            user = request.user
            # Ensure user is not a SimpleLazyObject
            if isinstance(user, SimpleLazyObject):
                user._setup()
                user = user._wrapped
            User = get_user_model()
            if isinstance(user, User):
                chat_message.sender = user
            else:
                return redirect('home')  # Handle case where user is not valid
            session_id = request.POST.get('session_id')
            if session_id:
                chat_message.session = get_object_or_404(CounselingSession, id=session_id)
            chat_message.save()
            if session_id:
                return redirect('chat_view', session_id=session_id)
    return redirect('home')

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    session_id = message.session.id
    if request.user == message.sender:
        message.delete()
    return redirect('chat_view', session_id=session_id)