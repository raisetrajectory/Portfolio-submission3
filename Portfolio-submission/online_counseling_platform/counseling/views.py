# counseling/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

from .models import Counselor, CounselingSession, ChatMessage
from .forms import CounselorForm, ProfileForm


def home(request):
    return render(request, 'home.html')

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(CounselingSession, id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'session_detail.html', {'session': session, 'messages': messages})

def chat_view(request):
    messages = ChatMessage.objects.all()
    try:
        template = get_template('counseling/registration/chat.html')
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist("The template 'counseling/registration/chat.html' does not exist.")
    return render(request, 'counseling/registration/chat.html', {'messages': messages})

@login_required
def create_session(request):
    if request.method == 'POST':
        counselor_id = request.POST.get('counselor')
        counselor = get_object_or_404(Counselor, id=counselor_id)
        session = CounselingSession.objects.create(user=request.user, counselor=counselor)
        return redirect('chat_view', session_id=session.id) # type: ignore

    counselors = Counselor.objects.all()
    return render(request, 'create_session.html', {'counselors': counselors})

def new_func():
    counselors = Counselor.objects.all()

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # ホームページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # ログアウト後にホームページにリダイレクト
    return render(request, 'logout.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def counselor_list_view(request):
    counselors = Counselor.objects.all()
    return render(request, 'counselor_list.html', {'counselors': counselors})

def chat(request):
    messages = ChatMessage.objects.all()
    return render(request, 'chat.html', {'messages': messages})

def get_messages(request):
    messages = ChatMessage.objects.values('user', 'content')
    return JsonResponse({'messages': list(messages)})

def send_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        ChatMessage.objects.create(user=request.user, content=message_content)
    return redirect('chat')