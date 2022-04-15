from django.shortcuts import  redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import UserRegisterForm


class MainLoginView(SuccessMessageMixin, LoginView):
    template_name="main/login.html"
    success_message = "You are logged in!!!"
    redirect_authenticated_user=True

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'main/register.html'
    success_url = reverse_lazy('main:login')
    form_class = UserRegisterForm
    success_message = "You are registered, now login."
    redirect_authenticated_user=True

    def get(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect('logs_list')
        return super().get(request, *args, **kwargs)
