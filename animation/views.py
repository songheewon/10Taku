from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Genre, Animation
from user.models import UserModel
from django.db.models import Q
from detail.models import Recommend, Bookmark
import random




def home(request):
    user = request.user.is_authenticated #유저는 인증된 유저이다.
    if user:
        return redirect('/main') #인증된유저가 있다면
    else:
        return redirect('/login') #인증된 유저가 없다면

# @login_required
# def main_view(request):
#     user = request.user
#     genres = user.fav_genre.all().values()
#
#     genre_list = []
#
#     for genre in genres:
#
#         genre_list.append(genre)
#
#
#
#     return render(request, 'animation/mainpage.html', {'my_genre': genre_list})

@login_required
def main_view(request):
    user = request.user
    main_genres = list(user.fav_genre.all())
    animation_list = Animation.objects.all()

    genre_ani_info = {}
    for main_genre in main_genres:
        # 그 장르가 있는 애니의 첫 6개만 가져오기
        search_list = list(animation_list.filter(Q(genre__name__icontains=main_genre.name)))
        random_list = random.sample(search_list, len(search_list))[:7]
        ani_info_list = []
        for animation in random_list:
            genres = Genre.objects.filter(animation__id=animation.id).values()
            genre_list = []
            for genre in genres:
                genre_list.append(genre['name'])
            genre_list = ", ".join(genre_list)
            ani_info = {'title': animation.title, 'img': animation.img, 'genre': genre_list, 'id': animation.id}
            ani_info_list.append(ani_info)

        genre_ani_info[main_genre] = ani_info_list
        #키값은 장르 오브젝트, 밸류값을 리스트<< 안의 객체들은 딕셔너리가 7개
    # print(genre_ani_info) #딕셔너리고
    # print(genre_ani_info.items()) #튜플형태로 변형


    return render(request, 'animation/mainpage.html', {'genre_ani_info': genre_ani_info.items()})

@login_required
def genre_view(request, id):
    user = request.user
    genre = Genre.objects.get(id=id)
    same_genre = Animation.objects.filter()
    print(same_genre)

    return render(request, 'animation/genrepage.html', {'genre': genre})


@login_required
def show_recommend_view(request):
    user = request.user
    recommends = Recommend.objects.filter(user=user)
    ani_info = {}

    for recommend in recommends:
        animation = recommend.animation
        genres = Genre.objects.filter(animation__id=animation.id).values()
        genre_list = []
        for genre in genres:
            genre_list.append(genre['name'])

        genre_list = ", ".join(genre_list)

        ani_info[animation.title] = {
            'id': animation.id,
            'img': animation.img,
            'genres': genre_list,
        }


    return render(request, 'animation/my_recommend.html', {'ani_info': ani_info.items()})


@login_required
def show_bookmark_view(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)
    print(bookmarks)
    ani_info = {}
    for bookmark in bookmarks:
        animation = bookmark.animation
        genres = Genre.objects.filter(animation__id=animation.id).values()
        genre_list = []
        for genre in genres:
            genre_list.append(genre['name'])

        genre_list = ", ".join(genre_list)

        ani_info[animation.title] = {
            'id': animation.id,
            'img': animation.img,
            'genres': genre_list
        }

    print(ani_info.items())

    return render(request, 'animation/bookmark.html', {'ani_info': ani_info.items()})


@login_required
def search_view(request):
    animation_list = Animation.objects.all()
    search = request.GET.get('search', '')
    if search:
        search_list = animation_list.filter(Q(title__icontains=search)) #제목검색
        ani_info = []
        print(search_list)

        for anime in search_list:
            img = animation_list.get(id=anime.id).img
            title = animation_list.get(id=anime.id).title
            genres = Genre.objects.filter(animation__id=anime.id).values()
            genre_list = []
            for genre in genres:
                genre_list.append(genre['name'])
            genre_list = ", ".join(genre_list)
            dic = {'img': img, 'title': title, 'genre': genre_list, 'id': anime.id}
            ani_info.append(dic)


        return render(request, 'animation/search_result.html', {'search': search, 'ani_info': ani_info})
    return render(request, 'animation/search_result.html')

