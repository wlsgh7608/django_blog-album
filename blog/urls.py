from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('',PostLV.as_view(),name = 'index'),
    #  /post/
    path('post/',PostLV.as_view(),name = 'post_list'),
    #  /post/django-example/
    path('post/<slug:slug>/',PostDV.as_view(),name = 'post_detail'),
    # /archive/
    path('archive/',PostAV.as_view(),name = 'post_archive'),
    # /2021
    path('<int:year>/',PostYAV.as_view(),name = 'post_year_archive'),
    # /2021/no
    path('<int:year>/<str:month>/',PostMAV.as_view(),name = 'post_month_archive'),
    # 2021/nov/10
    path('<int:year>/<str:month>/<int:day>',PostDAV.as_view(),name = 'post_day_archive'),
    # today
    path('today/',PostTAV.as_view(),name= 'post_today_archive'),

    path('tag/',TagCloudTV.as_view(),name= 'tag_cloud'),
    path('tag/<str:tag>/',TaggedObjectLV.as_view(),name = 'tagged_object_list'),

    path('search/',SearchFormView.as_view(),name = 'search'),

    path('add/',PostCreateView.as_view(),name = 'add'),
    path('change/',PostChangeLV.as_view(),name = 'change'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name = 'update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'delete'),


]