from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUserForm, EditProfileForm


class LoginVeiw(View):
    def get(self, request):
        form = AuthenticationForm()
        ctx = {
            "form": form
        }
        return render(request, 'users/login.html', ctx)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"You have successfully logged in")
            return redirect('goodreads')
        else:
            return render(request, 'users/login.html', ctx)


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        ctx = {
            'form': form
        }
        return render(request, 'users/register.html', ctx)

    # def post(self, request):   # formasiz ishlatish
    #     data = request.POST
    #     username = data.get('username')
    #     email = data.get('email')
    #     password = data.get('password')
    #
    #     user = User.objects.create(
    #         username=username,
    #         email=email,
    #     )
    #     user.set_password(password)
    #     user.save()
    #     return redirect('users:login')

    def post(self, request):  # forma bilan ishlatish
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            ctx = {
                'form': form
            }
            return render(request, 'users/register.html', ctx)


class UsersProfileView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {
            'user': request.user
        }
        return render(request, 'users/profile.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(self.request)
        messages.info(request, f"You have successfully logged out")
        return redirect('goodreads')


class EditProfile(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'users/edit_profile.html', ctx)

    def post(self, request):
        form = EditProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        ctx = {
            "form": form
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile has successfully edited")
            return redirect('users:profile')
        else:
            return render(request, 'users/edit_profile.html', ctx)
