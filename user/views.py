from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/sign_up.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '') #None은 유저네임이없다면 빈칸으로 처리하겠다.
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password != password2:
            print('password')
            return render(request, 'user/sign_up.html', {'error': '비밀번호를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                print('빈칸')
                return render(request, 'user/sign_up.html', {'error': '사용자 이름과 비밀번호는 필수 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                print('사용자 존재!')
                return render(request, 'user/sign_up.html', {'error': '사용자가 존재합니다'}) #사용자가 존재하기 때문에 저장x 회원가입페이지 다시띄움
            else:
                UserModel.objects.create_user(username=username, password=password, email=email) #밑의 주석코드를 한줄로 줄임
                print('회원가입 성공')
                return redirect('/login')


# 로그인 기능
def login_view(request): #sign_in_view 함수 (요청받은 정보 request)
    if request.method == 'POST': #메소드는 POST다.
        username = request.POST.get('username', '') #유저ID 입력받는다.
        password = request.POST.get('password', '') #비밀번호 입력받는다.

        me = auth.authenticate(request, username=username, password=password) #인증모듈 authenticate

        if me is not None: #위의 코드에서 사용자 정보를 다비교하고 오기때문에 me만 사용한다. me가 비어있지않다면
            auth.login(request, me) #내정보를 넣어준다.로그인 작업을 해준다.
            print('로그인성공')
            return redirect('/')  #기본 url로 redirect
        else:
            print('로그인실패')
            return render(request, 'user/login.html', {'error': '유저이름 혹은 비밀번호를 확인 해 주세요'})

    elif request.method == 'GET': #메소드 GET
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/login.html') #로그인페이지를 띄워준다.



@login_required   #사용자가 로그인이 꼭 되어있어야만 접근이 가능한 함수다.
def logout(request):
    auth.logout(request)
    return redirect('/')
