from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.dates import DayArchiveView,YearArchiveView,MonthArchiveView
from django.views.generic.dates import ArchiveIndexView,TodayArchiveView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from blog.forms import PostSearchForm
from django.db.models import Q
from blog.models import Post
from tagging.models import Tag,TaggedItem
from tagging.views import TaggedObjectList

from mysite.views import LoginRequiredMixin
# Create your views here.

#  ListView
# ListView 제네릭 뷰를 상속받아 PostLV 클래스형 뷰를 정의, 
# ListView 제네릭 뷰는 테이블로부터 객체리스트를 가져와 그 리스트 출력
class PostLV(ListView):
    model = Post # PostLV 클래스의 대상 테이블
    template_name= 'blog/post_all.html' # 템플릿 파일 지정, default: blog/post_list.html
    context_object_name = 'posts' # 템플릿 파일로 넘겨주는 객체리스트에 대한 컨텍스트 변수명 'posts', default : object_list
    paginate_by = 2 # 한 페이지에 보여주는 객체리스트의 숫자 , 페이징 기능 사용 가능

# Detailview
# DetailView 제네릭 뷰를 상속받아 PostDV 클래스형 뷰를 정의
# 테이블로부터 특정 객체를 가져와 그 객체의 상세 정보 출력
# 특정 객체를 검색하기 위한 키는 기본 키 대신 slug 속성을 사용함
# slug 파라미터는 URLconf에서 추출해서 뷰를 넘겨줌
class PostDV(DetailView):
    model = Post # PostDV 클래스의 대상 테이블

# 테이블로부터 객체 리스트를 가져와, 날짜 필드를 기준으로 최신 객체 먼저 출력
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'
# 테이블로부터 날짜 필드의 연도를 기준으로 객체 리스트를 가져와 그 객체들이 속한 월을 리스트로 출력
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True # True : 해당 년도에 해당하는 객체의 리스트를 만들어 템플릿에 넘겨줌, default : False
# 테이블로부터 날짜 필드의 연월을 기준으로 객체 리스트를 가져와 리스트 출력
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_date'
    month_format="%m"
# 테이블로부터 날짜 필드의 연월일을 기준으로 객체 리스트를 가져와 리스트 출력
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_date'
    month_format= "%m"
# 테이블로부터 날짜 필드의 날짜가 오늘인 객체 리스트를 가져와 그 리스트 출력
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_date'


class TagCloudTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'

class TaggedObjectLV(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'

# FormView 제네릭 ㅂ를 상속받아 SEarchFormView 클래스형 뷰 정의
# FormView 제니릭 뷰는 GET요청인 경우 폼을 화면에 보여주고 사용자의 입력을 기다림
#  사용자가 폼에 데이터를 입력한 후 제출하면 이는 POST 요청으로 접수되어 FormView 클래스는 데이터에 대한 유효성 검사를 실시
# 데이터가 유효하면 form_valid()함수를 실행한 후에 적절한 URL로 리다이렉트하는 기능을 갖고 있음
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name= 'blog/post_search.html'

    # POST 요청의 search_word 파라미터 값을 추출하여 schWord 변수에 지정, search_wrod 파라미터는 PostSearchForm 클래스에서 정의한 id
    def form_valid(self,form):
        schWord = "%s" %self.request.POST['search_word']
        # icontains = 대소문 구분안하고 조사, distinct() 중복 제거
        post_list = Post.objects.filter(Q(title__icontains=schWord)|Q(description__icontains=schWord)|Q(content__icontains=schWord)).distinct()

        context ={}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list']=post_list
        return render(self.request,self.template_name,context)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','slug','description','content','tag']
    initial  = {'slug':'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(PostCreateView,self).form_valid(form)

class PostChangeLV(LoginRequiredMixin,ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self) :
        return Post.objects.filter(owner = self.request.user)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title','slug','description','content','tag']
    success_url = reverse_lazy('blog:index')
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
