from django.db.models.fields.files import ImageField, ImageFieldFile # 장고 기본필드인 ImageField, ImageFieldFIle 클래스 임포트
from PIL import Image # 파이썬 이미지 처리 라이브러리 PIL.image 임포트
import os

def _add_thumb(s):
    """
    기존 이미지 파일명 기준으로 썸네일 이미지 파일명을 만들어줌
    ex) abc.jpg -> abc.thumb.jpg
    """
    parts = s.split('.')
    parts.insert(-1,'thumb')
    # 이미지 확장자를 jpg로 변경
    if parts[-1].lower() not in ['jpeg','jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):
    """
    ImageFieldFile 상속받음.
    이 클래스는 파일 시스템에 직접 파일을 쓰는 지우는 작업을 함
    """
    def _get_thumb_path(self):
        """"
        이미지를 처리하는 필드는 파일의 경로(path)와 URL(url) 속성을 제공
        원본 파일의 경로인 path 속성에 추가해 썸네일 경로인 thumb_path 속성을 만듦
        """
        return _add_thumb(self.path)

    def _get_thumb_url(self):

        return _add_thumb(self.url)
    thumb_path = property(_get_thumb_path)
    thumb_url = property(_get_thumb_url)

    # 파일 시스템에 파일을 저장하고 생성하는 메소드
    def save(self,name,content,save = True): 
        super(ThumbnailImageFieldFile,self).save(name,content,save) # 부모 ImageFielidFile 클래스의 save() 메소드를 호출하여 원본 이미지 저장
        img = Image.open(self.path)
        img = img.convert("RGB")
        img.save(self.path)
        size = (128,128) # 원본 파일로부터 128x128 크기의 썸네일 이미지 생성
        img.thumbnail(size,Image.ANTIALIAS)
        background = Image.new('RGB',size,(255,255,255,0)) # 이미지 색상 흰색, 완전 불투명한 이미지 
        background.paste(
            img,(int((size[0] - img.size[0])/2),int((size[1]-img.size[1])/2))) # 썸네일과 백그라운드 이미지를 합쳐서 정사각형 모양의 썸네일 이미지, 빈공간은 백그라운드 이미지에 의해 하얀색
        background.save(self.thumb_path,'JPEG') # 합쳐진 이미지를 jpeg 형식으로 파일 시스템의 thumb_path 경로에 저장
    
    def delete(self,asve =True): 
        """
        delete 메소드 호출 시 원본이미지 뿐만 아니라 썸네일 이미지 삭제
        """
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile,self).delete(save)
    
# ImageField 상속받음
class ThumbnailImageField(ImageField): 
    attr_class = ThumbnailImageFieldFile # 새로운 filefield 클래스를 정의할 때는 그에 상응하는 file 처리 클래스를 attr_class 속성에 지정필수

    def __init__(self,thumb_width =128,thumb_height = 128,*args,**kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField,self).__init__(*args,**kwargs)


