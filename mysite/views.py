from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
# 데코레이터로 사용하는 함수로 일반 함수에 적용, 로그인 한 경우는 원래 함수 실행, 로그인 X -> 로그인페이지 리다이렉트
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    # TemplateView을 사용하는 경우 template_name 클래스 변수를 오버라디이
    template_name= 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    # reverse,reverse_lazy 함수는 인자로 url 패턴명을 받음.
    # reverse_lazy : views.py 모듈이 로딩되고 처리되는 시점에 urls.py 모듈이 로딩되지 않을 수 있으므로 reverse_lazy사용
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)