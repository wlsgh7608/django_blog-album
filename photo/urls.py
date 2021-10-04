from django.contrib import admin
from django.urls import path,include
from photo.views import *
app_name = 'photo'
urlpatterns = [
    path('',AlbumLV.as_view(),name = 'index'),
    path('album/',AlbumLV.as_view(),name = 'album_list'),
    path('album/<int:pk>/',AlbumDV.as_view(),name = 'album_detail'),
    path('photo/<int:pk>/',PhotoDV.as_view(),name = 'photo_detail'),

    path('album/add/',AlbumPhotoCV.as_view(),name = 'album_add'),
    path('album/change/',AlbumPhotoLV.as_view(),name = 'album_change'),
    path('album/<int:pk>/update/',AlbumPhotoUV.as_view(),name = 'album_update'),
    path('album/<int:pk>/delete/',AlbumDeleteView.as_view(),name = 'album_delete'),
    
    path('photo/add',PhotoCreateView.as_view(),name = 'photo_add'),
    path('photo/change',PhotoChangeLV.as_view(),name = 'photo_change'),
    path('photo/<int:pk>/update',PhotoUpdateView.as_view(),name = 'photo_update'),
    path('photo/<int:pk>/delete',PhotoDeleteView.as_view(),name = 'photo_delete'),

]
