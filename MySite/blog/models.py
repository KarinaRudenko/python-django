from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class New(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    deck = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', blank=True, null=True)


    def get_absolute_url(self):
        return f'/news/{self.id}'

class Comment(models.Model):
    post = models.ForeignKey(New,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
