from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView,UpdateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import UserForm
from django.views import View


class UserUpdate(LoginRequiredMixin,UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user_edit.html'
    success_url = '/news/'

    def get_object(self, **kwargs):
        return self.request.user




class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


