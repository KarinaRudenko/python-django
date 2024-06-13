from django.contrib.auth.decorators import login_required
from django.views import View

from .forms import CommentForm, NewForm
from .models import New, Comment
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm


class NewsDeleteView(DeleteView):
    model = New
    success_url = '/news/'
    template_name = 'blog/news_delete.html'
    form_class = NewForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('blog-home')

class NewsUpdateView(UpdateView):
    model = New
    template_name = 'blog/create.html'
    form_class = NewForm

def create(request):
    error = ''
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog-home')  # Используйте правильное имя URL-шаблона
        else:
            error = 'Ошибка'
    form = NewForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'blog/create.html', data)

class ChangeFormView(UpdateView):
    form_class = PasswordChangeForm
    template_name = 'blog/edit_pass.html'
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(ChangeFormView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs

def search_news(request):
    query = request.GET.get('search_text')
    news = New.objects.filter(title__icontains=query)
    return render(request, 'blog/search.html', {'news': news, 'query': query})

def home(request):
    data = {
        'news': New.objects.order_by('-data')[:3],
        'title': 'Главная страница'
    }
    return render(request, 'blog/home.html', data)

def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Контакты'})

@login_required
def profile(request):
    user_comments = Comment.objects.filter(name=request.user.username)
    return render(request, 'blog/profile.html', {
        'title': 'Профиль',
        'user_comments': user_comments
    })

class NewsDT(DetailView):
    model = New
    template_name = 'blog/novosti.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(active=True)
        new_comment = None
        if self.request.method == 'POST':
            comment_form = CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        else:
            comment_form = CommentForm()
        context['comments'] = comments
        context['new_comment'] = new_comment
        context['comment_form'] = comment_form
        return context

class NewsDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(New, pk=pk)
        comments = post.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm()
        return render(request, 'blog/novosti.html', {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        })

    def post(self, request, pk):
        post = get_object_or_404(New, pk=pk)
        comments = post.comments.filter(active=True)
        new_comment = None
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return render(request, 'blog/novosti.html', {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        })

def news(request):
    data = {
        'news': New.objects.order_by('-data'),
        'title': 'Новости'
    }
    return render(request, 'blog/blog.html', data)

class DataMixin:
    pass

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('blog-home')

    def getcontextdata(self, *, objectlist=None, **kwargs):
        context = super().getcontextdata(**kwargs)
        cdef = self.getusercontext(title="Perистрация")
        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

def logout_user(request):
    logout(request)
    return redirect('login')

