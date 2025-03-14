from django.contrib import admin
from . import models

# Register your models here.
class blog_admin(admin.ModelAdmin):
    list_display = ('id','title', 'created_date', 'published_date', 'status' , 'image', 'category_name')


admin.site.register(models.category)
admin.site.register(models.blog, blog_admin)
admin.site.register(models.contact)