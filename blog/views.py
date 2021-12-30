from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Comment, Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context )

def LikeView(request, pk):
    post = Post.objects.get(id=pk)
    post.likes.add(request.user)
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
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        context['total_likes']= total_likes
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title','description','header_image','content' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post 
    fields = ['title','description','content']

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


class PostCommentView(CreateView):
	model = Comment
	form_class = CommentForm
	ordering = ['-date_added']


	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

	success_url = '/'

	

