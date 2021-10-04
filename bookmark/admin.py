from django.contrib import admin
from bookmark.models import BookMark
# Register your models here.

class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['title','url']

admin.site.register(BookMark,BookMarkAdmin)
