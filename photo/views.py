from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from photo.forms import PhotoInlineFormSet
# 인파인 폼셋이란 메인 폼에 딸려 있는 폼셋, 테이블 관계가 1:N인 경우 N 테이블의 레코드 여러개를 한꺼번에 입력받기 위함
from photo.models import Photo,Album

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from mysite.views import LoginRequiredMixin
# Create your views here.
class AlbumLV(ListView):
    model = Album

class AlbumDV(DetailView):
    model = Album

class PhotoDV(DetailView):
    model = Photo



class PhotoCreateView(LoginRequiredMixin,CreateView):
    model = Photo
    fields = ['album','title','image','description']
    success_url = reverse_lazy('photo:index')
    
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(PhotoCreateView,self).form_valid(form)
    
class PhotoChangeLV(LoginRequiredMixin,ListView):
    template_name = 'photo/photo_change_list.html'
    
    def get_queryset(self) :
        return Photo.objects.filter(owner = self.request.user)
    
class PhotoUpdateView(LoginRequiredMixin,UpdateView):
    model = Photo
    fields = ['album','title','image','description']
    success_url = reverse_lazy('photo:index')
class PhotoDeleteView(LoginRequiredMixin,DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')

# Album
class AlbumPhotoCV(LoginRequiredMixin,CreateView):
    model = Album
    fields = ['name','description']
    template_name = 'photo/album_form.html'
    
    # default context ㅚ에 추가적인 context 변수를 정의하기 위하여 오버라이딩
    def get_context_data(self, **kwargs):
        # AlbumPhotoCV 부모 클래스의 get_context_data() 호출하여 기본 컨텍스트 설정
        context = super(AlbumPhotoCV,self).get_context_data(**kwargs) 
        if self.request.POST: # POST 인경우
            context['formset'] = PhotoInlineFormSet(self.request.POST,self.request.FILES) # request.POSt와 request.FILES 파라미터를 사용하여 지정
        else: # GET 요청인 경우
            context['formset'] = PhotoInlineFormSet()
        return context

    def form_valid(self,form):
        form.instance.owner = self.request.user # form owner 필드에는 현재 로그인된 사용자의 User 객체 할당,
        context = self.get_context_data()# 앞에서 정의한 context_data호출하여 context 컨텍스트 지정
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user# 각 폼의 owner 필드에 현재 로그인된 사용자의 User 객체 할당
        
        if formset.is_valid(self,form): # 각 사진 폼의 데이터가 모두 유효한지 확인
            self.object = form.save() # form.save을 호출하여 폼의 데이터를 테이블에 저장, 즉 앨범 레코드 하나 생성
            formset.instance = self.object #폼셋의 메인객체를 방금 테이블에 저장한 객체로 지정 
            formset.save() #폼셋의 데이터를 테이블에 저장 
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AlbumPhotoUV(LoginRequiredMixin,UpdateView):
    model = Album
    fields = ['name','description']
    template_name = 'photo/album_form.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumPhotoUV,self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.reqeust.POST,self.request.FILES,instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context
    
    def form_valid(self,form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    
class AlbumPhotoLV(LoginRequiredMixin,ListView):
    template_name = 'photo/album_change_list.html'
    
    def get_queryset(self) :
        return Album.objects.filter(owner = self.request.user)
    
class AlbumDeleteView(LoginRequiredMixin,DeleteView):
    model = Album
    success_url = reverse_lazy('album:index')