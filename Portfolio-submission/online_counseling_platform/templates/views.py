from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage  # type: ignore # チャットメッセージのモデルをインポート
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

def home(request):
    return render(request, 'home.html')

def login_view(request):
    # ログインのロジック
    return render(request, 'login.html')

@login_required
def chat_view(request):
    messages = ChatMessage.objects.all()  # チャットメッセージを取得
    try:
        template = get_template('counseling/registration/chat.html')
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist("The template 'counseling/registration/chat.html' does not exist.")
    return render(request, 'counseling/registration/chat.html', {'messages': messages})
