from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import fields
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Comment, Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from blog import models

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context )

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:    
        post.likes.add(request.user)
        liked = True
        
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostListView(ListView):
    model = Post 
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_added']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post 
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_added')

class PostDetailView(DetailView):
    model = Post 

    def get_context_data(self, *args,**kwargs):
        
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()
        
        liked = False
        if post.likes.filter(id=self.request.user.id).exists:
            liked = True
        
        context['total_likes']= total_likes
        context['liked']= liked
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title','description','header_image','content' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post 
    fields = ['title','description','header_image','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/' 
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['post_pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.kwargs['post_pk']})

class PostCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['post_pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.kwargs['post_pk']})
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostCommentDeleteView(DeleteView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
    def get_success_url(self):
        return reverse_lazy('post-detail',kwargs={'pk':self.kwargs['post_pk']})    


def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(title__icontains=searched)
        posts = Post.objects.filter(description__icontains=searched)
        return render(request, 'blog/search.html', {'searched':searched, 'posts':posts})
    else:
        return render(request, 'blog/search.html', {})    
    

    

