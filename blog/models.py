from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=100)
    header_image = models.ImageField(null=True,blank=True, upload_to="images/")
    content = HTMLField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    description = models.CharField(max_length=255, default='Click above this for the full post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
   
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)

