from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import *
from .forms import PostForm
from .filters import PostFilter
from django.urls import reverse_lazy
from django.views import View
from .tasks import hello, send_mail_for_sub_test



class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'News.html'
    context_object_name = 'News'
    paginate_by = 2
    form_class =PostForm

class Post_Filter(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'search.html'
    context_object_name = 'News'
    paginate_by = 3
    form_class =PostForm


    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=PostFilter(self.request.GET,queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'New'

class PostCreate(PermissionRequiredMixin,CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('newapp.add_post',)

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = 2
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('newapp.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')


class AddNews(PermissionRequiredMixin, CreateView):
    permission_required = ('newapp.add',)


class ChangeNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('newapp.edit',)


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('newapp.delete',)

class CategoryList(ListView):
    model = Category
    template_name = 'subscription_list.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('name')

class IndexView(View):
    def get(self, request):
        # printer.apply_async([10], countdown=10)
        # hello.delay()
        send_mail_for_sub_test.delay()
        return HttpResponse('Hello!')

