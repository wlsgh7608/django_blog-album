from django.shortcuts import render
from django.views.generic import ListView,DetailView
from bookmark.models import BookMark

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from mysite.views import LoginRequiredMixin

# Create your views here.

#  ListView
class BookMarkLV(ListView):
    model = BookMark

# DetailView
class BookMarkDV(DetailView):
    model = BookMark

class BookMarkCreateView(LoginRequiredMixin,CreateView):
    model = BookMark
    fields = ['title','url']
    success_url = reverse_lazy('bookmark:index')
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(BookMarkCreateView,self).form_valid(form)

class BookmarkUpdateView(LoginRequiredMixin,UpdateView):
    model = BookMark
    fields = ['title','url']
    success_url = reverse_lazy('bookmark:index')


class BookMarkChangeView(LoginRequiredMixin,ListView):
    template_name = 'bookmark/bookmark_change_list.html'
    
    def get_queryset(self) :
        return BookMark.objects.filter(owner = self.request.user)
    

class BookMarkDeleteView(LoginRequiredMixin,DeleteView):
    model = BookMark
    success_url = reverse_lazy('bookmark:index')

