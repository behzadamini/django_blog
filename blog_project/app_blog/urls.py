from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('blog/', views.blog_home, name='blog-home'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog-detail'),
]