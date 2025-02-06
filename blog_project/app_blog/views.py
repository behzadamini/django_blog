from django.shortcuts import render, get_object_or_404,HttpResponse
from django.utils import timezone
from . import models

def home(request):
    return render(request, 'app_blog/index.html')

def blog_home(request):
    posts = models.blog.objects.filter(status=True, published_date__lte = timezone.now())
    context = {'posts': posts}
    return render(request, 'app_blog/blog-home.html', context)

def blog_detail(request, blog_id):
    post = get_object_or_404(models.blog, pk=blog_id)
    if post:
        post.counted_views += 1
        post.save()
        context = {'post': post}
        return render(request, 'app_blog/blog-single.html', context)
    else:
        context = {'post': None}
        return HttpResponse('Blog not found', status=404, content=context)
    
    