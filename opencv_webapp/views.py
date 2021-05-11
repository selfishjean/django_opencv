from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .cv_functions import cv_detect_face

# Create your views here.

def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})



def simple_upload(request):

    if request.method == 'POST': # 사용자가 form 태그 내부의 submit 버튼을 클릭하여 데이터를 제출했을 시

        # print(request.POST) : 타이틀 <QueryDict: {'csrfmiddlewaretoken': [‘csrf_token 임시 비밀번호’], 'title': ['upload_1']}>
        # print(request.FILES) : 이미지 <MultiValueDict: {'image': [<InMemoryUploadedFile: ses.jpg (image/jpeg)>]}>

        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = SimpleUploadForm(request.POST, request.FILES) # 빈 양식을 만든 후 사용자가 업로드한 데이터를 채워서 양식을 만듦


        if form.is_valid():

            myfile = request.FILES['image'] # 'image' : HTML input tag의 name attributes 값 : 'ses.jpg'

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # 경로명을 포함한 파일명 & 파일 객체

            # 업로드된 이미지 파일의 URL을 얻어내 Template에게 전달
            uploaded_file_url = fs.url(filename)

            # print(myfile) : ses.jpg
            # print(myfile.name) : ses.jpg
            # print(filename) : ses.jpg
            # print(uploaded_file_url) : media/ses.jpg

            context = {'form': form, 'uploaded_file_url': uploaded_file_url} # filled form
            return render(request, 'opencv_webapp/simple_upload.html', context)


    else: # request.method == 'GET' (DjangoBasic 실습과 유사한 방식입니다.)
        form = SimpleUploadForm() # empty form
        context = {'form': form}
        return render(request, 'opencv_webapp/simple_upload.html', context)




def detect_face(request):

    if request.method == 'POST' : # post 요청 처리

        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES) # filled form

        if form.is_valid():

            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경하거나 추가로 다른 데이터를 추가할 수 있음
            post = form.save(commit=False)
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장

            imageURL = settings.MEDIA_URL + form.instance.document.name # imageURL = post.document.url 동일
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # ./media/images/2021/05/10/nell.jpg

	        # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당

            # form.instance : ImageUploadModel Object (1) : DB 파일 하나의 행
            # form.instance.document : images/2021/05/10/nell.jpg
            # form.instance.document.name : images/2021/05/10/nell.jpg
            # form.instance.document.url : images/2021/05/10/nell.jpg

            # post : ImageUploadModel Object (1)
            # post.document : images/2021/05/10/nell.jpg
            # post.document.url : /media/images/2021/05/10/nell.jpg : 실제 이미지 경로 settings.py 에 있는 url 합쳐서 나옴

            # settings.MEDIA_URL : /media/
            # settings.MEDIA_ROOT_URL : . 최상위 폴더

            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)

    else: # get 요청 처리
         form = ImageUploadForm() # empty form
         return render(request, 'opencv_webapp/detect_face.html', {'form':form})
