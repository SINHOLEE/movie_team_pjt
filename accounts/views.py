from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash #update_session_auth_hash: 비밀번호 수정해도 자동로그아웃 되지 않도록
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated: 
        return redirect('movies:index')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else: 
        form = CustomUserCreationForm()
    context = {'form':form,}
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        # 로그인 로직
        form = AuthenticationForm(request, request.POST) 
        if form.is_valid():
            auth_login(request, form.get_user())
            next_page = request.GET.get('next')
            return redirect(next_page or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form':form,}
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:index')


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else: 
        form = CustomUserChangeForm(instance=request.user) 
    context = {'form':form,}
    return render(request,'accounts/form.html', context)



@login_required 
def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,}
    return render(request, 'accounts/pwform.html', context)
        
