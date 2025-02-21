from django.shortcuts import render, get_object_or_404,HttpResponse
from django.utils import timezone
from . import models
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    return render(request, 'app_blog/index.html')

def blog_home(request, cat='', user=''):

    filters = Q(status=True, published_date__lte = timezone.now())

    if cat != '':
        filters &= Q(category__name=cat)

    if user != '':
        filters &= Q(author__username=user)
    
    posts = models.blog.objects.filter(filters).order_by('-pk')
    posts = Paginator(posts, 1)

    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    print(posts.__dict__)
    context = {'posts': posts}
    return render(request, 'app_blog/blog-home.html', context)

def blog_detail(request, blog_id):
    post = get_object_or_404(models.blog, pk=blog_id, status=True, published_date__lte = timezone.now())
    if post:
        post.counted_views += 1
        post.save()
        
        post_next = models.blog.objects.filter(status=True,pk__gt=post.pk, published_date__lte = timezone.now()).order_by('pk').first()
        post_prev = models.blog.objects.filter(status=True,pk__lt=post.pk, published_date__lte = timezone.now()).order_by('-pk').first()

        context = {
            'post': post,
            'post_next': post_next,
            'post_prev': post_prev,
            }

        return render(request, 'app_blog/blog-single.html', context)
    else:
        context = {'post': None}
        return HttpResponse('Blog not found', status=404, content=context)
    
    
def blog_search(request):
    filters = Q(status=True, published_date__lte = timezone.now())
    
    if str := request.GET.get('search'):
        filters &= Q(content__contains=str)
    
    posts = models.blog.objects.filter(filters).order_by('-pk')
    context = {'posts': posts}
    return render(request, 'app_blog/blog-home.html', context)
    
    