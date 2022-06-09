from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Genre, Animation
from user.models import UserModel
from django.db.models import Q
from detail.models import Recommend, Bookmark
import random
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def home(request):
    user = request.user.is_authenticated #유저는 인증된 유저이다.
    if user:
        return redirect('/main') #인증된유저가 있다면
    else:
        return redirect('/login') #인증된 유저가 없다면


@login_required
def main_view(request):
    user = request.user
    # 유저가 선택한 장르들 가져오기
    main_genres = list(user.fav_genre.all())
    animation_list = Animation.objects.all()


    # 키 = 장르 객체, 밸류 = 애니 정보 리스트가 담긴 딕셔너리 생성
    genre_ani_info = {}
    for main_genre in main_genres:
        # 각 장르마다 그 장르가 있는 애니들 모두 가져오기
        search_list = list(animation_list.filter(Q(genre__name__icontains=main_genre.name)))
        # 랜덤화하고 6개만 가져오기
        random_list = random.sample(search_list, len(search_list))[:6]

        # 각 장르마다 애니정보 딕셔너리들이 담길 리스트 생성
        ani_info_list = []
        # 각 애니마다 애니정보 딕셔너리 생성
        for animation in random_list:
            # 각 애니마다 그 애니의 장르들 모두 가져오기
            genres = Genre.objects.filter(animation__id=animation.id).values()
            # 리스트화 풀어주기
            genre_list = []
            for genre in genres:
                genre_list.append(genre['name'])
            genre_list = ", ".join(genre_list)
            ani_info = {'title': animation.title, 'img': animation.img, 'genre': genre_list, 'id': animation.id}
            ani_info_list.append(ani_info)

        genre_ani_info[main_genre] = ani_info_list

    # 유저 기반 추천 모델
    if len(Recommend.objects.filter(user__id=user.id)) > 0 and len(Recommend.objects.all()) > len(Recommend.objects.filter(user__id=user.id)):
        user_ratings = pd.DataFrame(list(Recommend.objects.all().values()))
        user_ratings.set_index('id', inplace=False)
        user_ratings = user_ratings[['user_id', 'animation_id']]
        user_ratings['rating'] = 1

        user_ratings = user_ratings.pivot_table('rating', index='user_id', columns='animation_id')
        user_ratings = user_ratings.fillna(0)
        user_based_collab = cosine_similarity(user_ratings, user_ratings)
        user_based_collab = pd.DataFrame(user_based_collab, index=user_ratings.index, columns=user_ratings.index)
        print(user_based_collab)
        print(user_based_collab[user.id])
        user = user_based_collab[user.id].sort_values(ascending=False).index[1]
        result = user_ratings.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)
        recommend_anis = list(result.keys())[:6]

        recommend_anis_list = []
        for recommend_ani in recommend_anis:
            recommend_anis_list.append(Animation.objects.get(id=recommend_ani))


        #템플렛으로 보내줄때는 key, value값을 꺼낼 수 있도록 애니정보의 딕셔너리 아이템들(튜플) 보내주기
        return render(request, 'animation/mainpage.html', {'genre_ani_info': genre_ani_info.items(), 'recommend_anis_list': recommend_anis_list})
    return render(request, 'animation/mainpage.html', {'genre_ani_info': genre_ani_info.items()})


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

    return render(request, 'animation/bookmark.html', {'ani_info': ani_info.items()})


@login_required
def search_view(request):
    animation_list = Animation.objects.all()
    search = request.GET.get('search', '')
    if search:
        search_list = animation_list.filter(Q(title__icontains=search)) #제목검색
        ani_info = []

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


def more_view(request, id):
    animation_list = Animation.objects.all()
    more_genre = Genre.objects.get(id=id)

    genre_ani_info = {}
    ani_info_list = []

    search_list = list(animation_list.filter(Q(genre__name__icontains=more_genre.name)))
    for animation in search_list:
        genres = Genre.objects.filter(animation__id=animation.id).values()
        genre_list = []
        for genre in genres:
            genre_list.append(genre['name'])
        print(genre_list)
        genre_list = ", ".join(genre_list)
        print(genre_list)
        ani_info = {'title': animation.title, 'img': animation.img, 'genre': genre_list, 'id': animation.id}
        ani_info_list.append(ani_info)

        genre_ani_info[more_genre] = ani_info_list

    return render(request, 'animation/genrepage.html', {'genre_ani_info': genre_ani_info.items()})