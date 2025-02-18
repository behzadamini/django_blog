from django import template
from django.db.models import Count, Q
from app_blog.models import blog
from django.utils import timezone

register = template.Library()

@register.simple_tag
def custom_tag():
    return "تمپلیت تگ ساده"

@register.filter(name='cu')
def custom_filter(value):
    return value[:8]


@register.inclusion_tag('app_blog/latest_post.html')
def latestpost():
    posts = blog.objects.filter(status=True, published_date__lte=timezone.now()).order_by('-pk')
    return {'posts': posts}

@register.inclusion_tag('app_blog/post_categories.html')
def postcategories():
    filters = Q(status=True, published_date__lte = timezone.now())
    categories = blog.objects.values('category__name').filter(filters).annotate(count=Count('id'))
    return {'cats': categories}

@register.inclusion_tag('app_blog/post_categories_list1.html')
def post_categories_list():
    filters = Q(status=True, published_date__lte = timezone.now())
    categorise = blog.objects.values('category__name').filter(filters).distinct()
    return {'cats': categorise}