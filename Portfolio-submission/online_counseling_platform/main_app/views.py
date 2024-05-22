from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def register(request):
    # ユーザー登録のロジック
    return render(request, 'register.html')

def chat(request):
    # チャット画面のロジック
    return render(request, 'chat.html')

def login_view(request):
    # ログインのロジック
    return render(request, 'login.html')

def logout_view(request):
    # ログアウトのロジック
    return redirect('home')

def profile(request):
    # プロフィール画面のロジック
    return render(request, 'profile.html')

def counselor_list(request):
    # カウンセラー一覧画面のロジック
    return render(request, 'counselor_list.html')
