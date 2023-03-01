from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView as PasswordChangeViewBasic, \
    PasswordResetCompleteView as PasswordResetCompleteViewBasic, LoginView as LoginViewBasic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from lifetable.forms import UserCreateForm, AuthenticationForm
from lifetable.models import User


class CreateUserView(CreateView):
    template_name = 'lifetable/register.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('ecogenius')

    def get_success_url(self):
        return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        is_student = User.objects.filter(is_student=False).exists()
        return form_class(is_student=is_student, **self.get_form_kwargs())

    def form_valid(self, form):
        response = super(CreateUserView, self).form_valid(form=form)
        login(self.request, form.instance)
        return response


class PasswordChangeView(PasswordChangeViewBasic):
    def get(self, request, *args, **kwargs):
        return redirect('home')


class PasswordResetCompleteView(PasswordResetCompleteViewBasic):
    def get(self, request, *args, **kwargs):
        return redirect('home')


class LoginView(LoginViewBasic):
    form_class = AuthenticationForm


class Home(View):
    def get(self, request, *args, **kwargs):
        return redirect('list_answer')
