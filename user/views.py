from django.shortcuts import render, redirect
from .models import UserModel
from animation.models import Genre
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/sign_up.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
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
                return render(request, 'user/sign_up.html', {'error': '사용자가 존재합니다'})
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
                print('회원가입 성공')
                return redirect('/login')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)

        if me is not None:
            auth.login(request, me)
            print('로그인성공')
            return redirect('/select_genre')
        else:
            print('로그인실패')
            return render(request, 'user/login.html', {'error': '유저이름 혹은 비밀번호를 확인 해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')

        return render(request, 'user/login.html')


@login_required
def logout(request):

    user = request.user
    user.fav_genre.clear()  #로그아웃시 선택했던 장르 삭제
    auth.logout(request)

    return redirect('/')

@login_required
def select_genre_view(request):
    if request.method == 'POST':
        user = request.user
        genre = request.POST.get('genre', '')
        genres = Genre.objects.get(id=genre)

        exist = user.fav_genre.filter(users__fav_genre=genres).exists()
        my_genres = user.fav_genre.all().values()
        genre_count = user.fav_genre.all().count()
        genre_list = []

        if exist:
            user.fav_genre.remove(genres)
        else:
            if genre_count < 3:
                user.fav_genre.add(genres)
            else:
                messages.error(request, '이미 3개의 장르 선택함.')

        for my_genre in my_genres:
            genre_list.append(str(my_genre['id']))

        return render(request, 'user/select_genre.html', {'genre_list': genre_list, 'count': len(genre_list)})

    return render(request, 'user/select_genre.html')

