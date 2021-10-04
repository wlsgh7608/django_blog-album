from photo.models import Album,Photo
# 인라인 폼셋을 반환
from django.forms.models import inlineformset_factory

# 1:N 관계인 album과 Photo 테이블을 이용하여 사진 인라인 폼셋을 만듦
PhotoInlineFormSet = inlineformset_factory(Album,Photo,
    fields = ['image','title','description'],
    extra = 2)
