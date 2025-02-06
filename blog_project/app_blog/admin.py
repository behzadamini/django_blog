from django.contrib import admin
from . import models

# Register your models here.
class blog_admin(admin.ModelAdmin   ):
    list_display = ('title', 'content', 'created_date', 'published_date', 'status')

admin.site.register(models.blog, blog_admin)