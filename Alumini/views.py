from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import events,Posts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.

class LinkListView(ListView):
    model = events
    template_name = 'Alumini/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'eves'

def event(request):
    return render(request,"Alumini/events.html")

def gallery(request):
    return render(request,"Alumini/gallery.html")
def act(request):
    return render(request,"Alumini/act.html")
def help(request):
    return render(request,"Alumini/help.html")
def princi(request):
    return render(request,"Alumini/princi.html")
def about(request):
    return render(request,"Alumini/about.html")
@login_required
def blog(request):
    context = {
        'posts': Posts.objects.order_by('-date_posted')
    }
    return render(request, 'Alumini/blog.html', context)
class PostListView(ListView):
    model = Posts
    template_name = 'Alumini/blog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Posts
    template_name = 'Alumini/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Posts


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog')
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    def get_success_url(self):
        return reverse('blog')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    def get_success_url(self):
        return reverse('blog')

def contact(request):
    return render(request,'Alumini/contact.html')

def add(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Alumini-index")
    else:
        form = Postform()

    context = {'form':form}
    return render(request, 'Alumini/add.html', context)