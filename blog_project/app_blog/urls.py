from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_home, name='blog_home'),
    path('blog/category/<str:cat>', views.blog_home, name='blog_home'),
    path('blog/author/<str:user>', views.blog_home, name='blog_home'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/search/', views.blog_search, name='blog_search'),
    path('contact/', views.contact, name='contact')
]