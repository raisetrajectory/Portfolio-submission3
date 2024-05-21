# counseling/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Counselor
from .forms import CounselorForm
from .models import CounselingSession, Counselor

def home(request):
    return render(request, 'home.html')

@login_required
def create_session(request, counselor_id):
    counselor = get_object_or_404(Counselor, id=counselor_id)
    session = CounselingSession.objects.create(user=request.user, counselor=counselor)
    return redirect('session_detail', pk=session.pk)

@login_required
def session_detail(request, pk):
    session = get_object_or_404(CounselingSession, pk=pk)
    return render(request, 'session_detail.html', {'session': session})

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
