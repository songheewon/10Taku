from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from detail.models import Recommend, Bookmark, Animation
from animation.models import Genre


def home(request):
    user = request.user.is_authenticated #유저는 인증된 유저이다.
    if user:
        return redirect('/main') #인증된유저가 있다면
    else:
        return redirect('/login') #인증된 유저가 없다면


@login_required
def show_recommend_view(request):
    user = request.user
    recommends = Recommend.objects.filter(user=user).values()
    recommend_list = []


    if len(recommends) > 0:
        for recommend in recommends:
            animation = recommend['animation_id']
            animes = Animation.objects.get(id=animation)
            recommend_list.append(animes)
            genres = Genre.objects.filter(animation__id=animation).values()
            genre_list = []
            if len(genres) > 0:
                for genre in genres:
                    genre_list.append(genre)

                for genre in genre_list:
                    genres = genre['name']
                    print(genres)
                # genre_list = ", ".join(genre_list)
            else:
                genre_list = "장르 정보가 없습니다"
    else:
        recommend_list = "추천한 애니가 없습니다"


    return render(request, 'animation/my_recommend.html', {'animations': recommend_list, 'genres': genres})


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
            'genres': genre_list,
        }

    print(ani_info.items())

    return render(request, 'animation/bookmark.html', {'ani_info': ani_info.items()})
