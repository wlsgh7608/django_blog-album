from django.db import models

from django.urls import reverse
from tagging.fields import TagField

from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
    title = models.CharField('TITLE', max_length=50) # title 컬럼명 'TITLE' 최대 50글자
    # 제목의 별칭, unique옵션을 추가하여 특정 포스트 검색시 기본 키 대신에 사용,allow_unicode : 한글처리 가능
    # Slug : 페이지나 포스트를 설명하는 핵심단어의 집합
    slug = models.SlugField('SLUG',unique= True, allow_unicode=True,help_text='one word for title alias') 
    # help_text 해당 컬럼을 설명해주는 문구 폼 화면에 나타남,
    description = models.CharField('DESCRIPTION',max_length=100,blank=True,help_text='simple description text')
    content = models.TextField('CONTENT')
    # 날짜와 시간을 입력하는 dAtaTimeField, auto_now_add : 객체가 데이터베이스에 저장될 때 자동으로 시각을 기록
    create_date = models.DateTimeField('Craete Date',auto_now_add=True)
    modify_date = models.DateTimeField('Modify Date',auto_now=True)
    tag = TagField()
    owner = models.ForeignKey(User,null = True, on_delete= models.CASCADE)

    # 필드속성 외에 필요한 파라미터가 있으면, Meta 내부 클래스 정의 
    class Meta:
        # 테이블의 별칭을 단수와 복수로 가질 수 있음
        verbose_name = 'post' # 단수
        verbose_name_plural = 'posts' # 복수
        db_table = 'my_post' # db 테이블 이름, default = 앱명_모델명
        ordering = ('-modify_date',) #리스트 출력시 modify_date 기준으로 내림차순

    def __str__(self):
        return self.title  # 객체의 문자열을 객체 title로 표시
    
    # 메소드가 정의한 객체를 지칭하는 URL 반환
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=(self.slug,))
    
    # modify_date 컬럼을 기준으로 이전 포스트를 반환
    def get_previous_post(self):
        return self.get_previous_by_modify_date()

    # modify_date 컬럼을 기준으로 다음 포스트를 반환
    def get_next_post(self):
        return self.get_next_by_modify_date()

    def save(self,*args,**kwargs):
        # save 메소드 재정의, save()메소드는 모델 객체의 내용을 db에 저장하는 메소드
        # self.id을 확인해 False인 경우, 처음으로 저장하는 경우에만 slug필드를 자동으로 채워줌
        if not self.id:
            # slug 필드를 자동으로 채우기 위함
            self.slug = slugify(self.title,allow_unicode=True)
        super(Post,self).save(*args,**kwargs)