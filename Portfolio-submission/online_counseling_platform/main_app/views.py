from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def login_view(request):
    # ログインのロジック
    return render(request, 'login.html')

@login_required
def chat_view(request):
    return render(request, 'chat.html')

def register(request):
    # ユーザー登録のロジック
    return render(request, 'register.html')

# def chat(request):
#     # チャット画面のロジック
#     return render(request, 'chat.html')



def logout_view(request):
    # ログアウトのロジック
    return redirect('home')

def profile(request):
    # プロフィール画面のロジック
    return render(request, 'profile.html')

def counselor_list(request):
    # カウンセラー一覧画面のロジック
    return render(request, 'counselor_list.html')
