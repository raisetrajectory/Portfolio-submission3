from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage  # チャットメッセージのモデルをインポート
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .models import CounselingSession, ChatMessage, User


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


