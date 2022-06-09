from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Bookmark, Recommend
from animation.models import Animation, Genre
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np


#애니메이션 상세 페이지
@login_required
def animation_detail(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)
    animations = Animation.objects.all()
    genres = Genre.objects.filter(animation__id=id).values()

    genre_list = []

    if len(genres) > 0:
        for genre in genres:
            name = genre['name']
            genre_list.append(name)
        genre_list = ", ".join(genre_list)
    else:
        genre_list = "장르 정보가 없습니다"

    genre_name_list = []

    for anime in animations:
        info = anime.genre.values()
        temp = []
        for i in info:
            temp.append(i['name'])
        genre_name_list.append(temp)

    genre_name_list = list(map(str, genre_name_list))

    cv = CountVectorizer()

    genre_vector = cv.fit_transform(list(map(str, genre_name_list)))  # 장르 벡터화


    genre_dic = cv.vocabulary_  # {'sf': 0, '가족': 1 ....}의 dictionary 형태


    neighbors = NearestNeighbors(n_neighbors=10).fit(genre_vector)

    detailpage_contents_recommend = np.zeros((0, 10), int)

    genre_info = pd.DataFrame(
        genre_vector.toarray(),
        columns=list(sorted(genre_dic.keys(), key=lambda x: genre_dic[x]))
    )
    list_idx=animation.id-1 # 내가 만든 리스트는 0부터, DB는 1부터라서 안 맞는 거였음
    knn_dist, idx = neighbors.kneighbors([genre_info.iloc[list_idx, :]]) # 여기에 list_idx로 참조하면 DB는 list_idx+1값을 보니까 맞게 불러옴
    detailpage_contents_recommend = np.append(detailpage_contents_recommend, np.array(idx), axis=0)
    detailpage_contents_recommend = detailpage_contents_recommend.tolist()
    detailpage_contents_recommend = detailpage_contents_recommend[0]

    for idx in range(len(detailpage_contents_recommend)):
        detailpage_contents_recommend[idx] += 1

    same_genre_ani_list = []
    for recommend_ani_id in detailpage_contents_recommend:
        same_genre_ani = Animation.objects.get(id=recommend_ani_id)
        same_genre_ani_list.append(same_genre_ani)


    is_bookmark = Bookmark.objects.filter(user=user, animation=animation).exists()
    is_recommend = Recommend.objects.filter(user=user, animation=animation).exists()
    comments = Comment.objects.filter(animation=animation).order_by('-created_at')
    comment_count = len(Comment.objects.filter(animation=animation).order_by('-created_at'))

    return render(request, 'animation/detail.html', {
        'animation': animation,
        'genre': genre_list,
        'is_bookmark': is_bookmark,
        'is_recommend': is_recommend,
        'comments': comments,
        'comment_count': comment_count,
        'same_genre_ani_list': same_genre_ani_list,
    })

#댓글 달기
@login_required
def comment(request, id):
    if request.method == "POST":
        animation = Animation.objects.get(id=id)
        user = request.user
        content = request.POST.get('my-content', '')
        my_comment = Comment(animation=animation, author=user, content=content)
        my_comment.save()
        return redirect('/detail/' + str(id))

    return redirect('/detail/' + str(id))

#댓글 삭제
@login_required
def delete_comment(request, id):
    my_comment = Comment.objects.get(id=id)
    current_ani = my_comment.animation.id
    my_comment.delete()
    return redirect('/detail/' + str(current_ani))


#북마크 기능
@login_required
def bookmark(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)

    try:
        my_bookmark = Bookmark.objects.get(user=user, animation=animation)
        my_bookmark.delete()
    except Bookmark.DoesNotExist:
        my_bookmark = Bookmark(user=user, animation=animation)
        my_bookmark.save()
        return redirect('/detail/' + str(id))

    return redirect('/detail/' + str(id))



#추천하기 기능
@login_required
def recommend_toggle(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)

    try:
        my_recommend = Recommend.objects.get(user=user, animation=animation)
        my_recommend.delete()
        animation.recommend_count -= 1
        animation.save()

    except Recommend.DoesNotExist:
        my_recommend = Recommend(user=user, animation=animation) #새로운 객체 만들어서 저장
        my_recommend.save()
        animation.recommend_count += 1
        animation.save()
        return redirect('/detail/' + str(id))

    return redirect('/detail/' + str(id))


#랜덤 추천
@login_required
def random_view(request):
    page_num = random.randrange(1, 917)
    return redirect('/detail/' + str(page_num))




