from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage  # チャットメッセージのモデルをインポート

def home(request):
    return render(request, 'home.html')

def login_view(request):
    # ログインのロジック
    return render(request, 'login.html')

@login_required
def chat_view(request):
    messages = ChatMessage.objects.all()  # チャットメッセージを取得
    return render(request, 'counseling/registration/chat.html', {'messages': messages})


# def register(request):
#     # ユーザー登録のロジック
#     return render(request, 'register.html')

# def logout_view(request):
#     # ログアウトのロジック
#     return redirect('home')

# def profile(request):
#     # プロフィール画面のロジック
#     return render(request, 'profile.html')

# def counselor_list(request):
#     # カウンセラー一覧画面のロジック
#     return render(request, 'counselor_list.html')
