from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Bookmark, Recommend
from animation.models import Animation, Genre
import random
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors


#애니메이션 상세 페이지
@login_required
def animation_detail(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)
    animations = Genre.objects.all().values()
    genres = Genre.objects.filter(animation__id=id).values()
    genre_list = []

    if len(genres) > 0:
        for genre in genres:
            name = genre['name']
            genre_list.append(name)
        genre_list = ", ".join(genre_list)
    else:
        genre_list = "장르 정보가 없습니다"

    # for anime in animations:
    #     genre_name = anime['name']
    #     cv = CountVectorizer()
    #     genre_vector = cv.fit_transform(genre_name)  # 장르 벡터화, animations.genre 부분은 animation import해서 수정해야함
    #
    #     print(genre_vector)

    is_bookmark = Bookmark.objects.filter(user=user, animation=animation).exists()
    is_recommend = Recommend.objects.filter(user=user, animation=animation).exists()
    comments = Comment.objects.filter(animation=animation).order_by('-created_at')
    comment_count = len(Comment.objects.filter(animation=animation).order_by('-created_at'))

    #컨텐츠 기반 장르 5가지 추천 코드
    #협업필터링 유저추천 5가지 애니메이션 코드
    return render(request, 'animation/detail.html', {
        'animation': animation,
        'genre': genre_list,
        'is_bookmark': is_bookmark,
        'is_recommend': is_recommend,
        'comments': comments,
        'comment_count': comment_count
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




