from django.urls import path
from bookmark.views import *
app_name = 'bookmark'

urlpatterns = [
    path('bookmark/',BookMarkLV.as_view(),name='index'),
    path('bookmark/<int:pk>/', BookMarkDV.as_view(),name='detail'),

    path('add/',BookMarkCreateView.as_view(),name = 'add'),
    path('change/',BookMarkChangeView.as_view(),name = 'change'),
    path('<int:pk>/update/',BookmarkUpdateView.as_view(),name = 'update'),
    path('<int:pk>/delete/',BookMarkDeleteView.as_view(),name = 'delete'),
]