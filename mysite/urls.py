"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static # static 함수 임포트, static() : 정적 파일을 처리하는 뷰를 호출하도록 그에 맞는 url 패턴 리턴
from mysite.views import HomeView,UserCreateView,UserCreateDoneTV

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('admin/', admin.site.urls),
    path('bookmark/',include('bookmark.urls')),
    path('blog/',include('blog.urls')),
    path('photo/',include('photo.urls')),

    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register/',UserCreateView.as_view(),name= 'register'),
    path('accounts/register/done/',UserCreateDoneTV.as_view(),name = 'register_done'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # 기존 url 패턴에 static()함수가 반환하는 url 패턴 추각
# settings.MEDIA_URL로 정의된 /media/URL 요청이 오면 django.views.static.serve() 뷰 함수가 처리하고, 이 뷰 함수에 document_root = settings.MEDIA_ROOT 키워드 인자가 전달
"""
static() 함수 형식
static(prefix,view = django.view.static.serve , **kwargs)
"""
