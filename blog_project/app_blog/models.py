from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.db import models

class category(models.Model):
    name = models.CharField(max_length=150, null=False)
    def __str__(self):
        return self.name


class blog(models.Model):
    image = models.ImageField(upload_to='blog', default='blog/blog_default.jpg')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    # tags
    category = models.ManyToManyField(category)
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def category_name(self):
        return "\n".join([cat.name for cat in self.category.all()])

    @property
    def excert(self):
        return Truncator(self.content).words(50)

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.subject