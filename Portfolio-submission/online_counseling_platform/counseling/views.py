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

User = get_user_model()

# def home(request):
#     return render(request, 'home.html')

def home(request):
    # 特定の条件が満たされた場合にのみユーザーを作成します。
    if some_condition and not User.objects.filter(username='default_user').exists():
        User.objects.create_user(username='default_user', password='defaultpassword')
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

@login_required
def chat_view(request, session_id=None, counselor_id=None):
    session = None
    if session_id:
        session = get_object_or_404(CounselingSession, id=session_id)
    elif counselor_id:
        counselor = get_object_or_404(Counselor, id=counselor_id)
        session, created = CounselingSession.objects.get_or_create(user=request.user, counselor=counselor)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.session = session
            chat_message.save()
            return redirect('chat_view', session_id=session.id)
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

# def send_message(request):
#     if request.method == 'POST':
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             session_id = form.cleaned_data['session_id']
#             message_text = form.cleaned_data['message']
#             session = CounselingSession.objects.get(id=session_id)
#             user = request.user if request.user.is_authenticated else None
#             try:
#                 default_user = User.objects.get(username='default_user')
#             except User.DoesNotExist:
#                 default_user = None
#             sender = user if user else default_user
#             chat_message = ChatMessage(sender=sender, message=message_text, session=session)
#             chat_message.save()
#             messages = ChatMessage.objects.filter(session=session)
#             return render(request, 'counseling/registration/chat.html', {'form': form, 'messages': messages, 'session': session})
#     else:
#         form = ChatMessageForm()
#     return render(request, 'counseling/registration/chat.html', {'form': form})

def send_message(request):
    messages = []  # 初期値として空のリストを設定
    session = None  # 初期値としてNoneを設定

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            message_text = form.cleaned_data['message']
            session = CounselingSession.objects.get(id=session_id)
            user = request.user if request.user.is_authenticated else None
            sender = user if user else User.objects.get(username='default_user')
            chat_message = ChatMessage(sender=sender, message=message_text, session=session)
            chat_message.save()
            messages = ChatMessage.objects.filter(session=session)
            form = ChatMessageForm(initial={'session_id': session.id})  # フォームをリセットしてセッションIDを保持
        else:
            # フォームが無効な場合でもsessionを取得
            session_id = request.POST.get('session_id')
            if session_id:
                session = CounselingSession.objects.get(id=session_id)
                messages = ChatMessage.objects.filter(session=session)
    else:
        session_id = request.GET.get('session_id')
        if session_id:
            session = CounselingSession.objects.get(id=session_id)
            form = ChatMessageForm(initial={'session_id': session.id})
            messages = ChatMessage.objects.filter(session=session)
        else:
            form = ChatMessageForm()

    return render(request, 'counseling/registration/chat.html', {'form': form, 'messages': messages, 'session': session})

def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    session_id = message.session.id
    if request.user == message.sender:
        message.delete_message()  # delete_messageメソッドを呼び出す
    return redirect('chat_view', session_id=session_id)