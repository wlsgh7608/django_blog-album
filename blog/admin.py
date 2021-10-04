from django.contrib import admin
from blog.models import Post
# Register your models here.

# Post 클래스가 Admin 사이트에서 어떤 모습을 보여줄지를 정의하는 클래스
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','modify_date') # Post 객체를 보여줄 때 title과 modify_date 화면에 출력
    list_filter = ('modify_date',) # modify_date 컬럼을 사용하는 필터 사이드바를 보여주도록 지정
    search_fields = ('title','content') # 검색박스를 표시하고, 입력한 단어는 title과 content에서 검색
    prepopulated_fields = {'slug':('title',)} # slug필드는 title필드를 사용하여 미리 채워지도록 함

admin.site.register(Post,PostAdmin)
