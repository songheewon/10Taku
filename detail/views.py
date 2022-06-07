from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Bookmark, Recommend
from animation.models import Animation, Genre
from user.models import UserModel


# Create your views here.
def show_detail_view(request):
    return render(request, 'animation/detail.html')


@login_required
def animation_detail(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)
    genres = Genre.objects.filter(animation__id=id).values()
    genre_list = []
    if len(genres) > 0:
        for genre in genres:
            name = genre['name']
            genre_list.append(name)
        genre_list = ", ".join(genre_list)
    else:
        genre_list = "장르 정보가 없습니다"

    is_recommend = Recommend.objects.filter(user=user, animation=animation).exists()

    #컨텐츠 기반 장르 5가지 추천 코드
    #협업필터링 유저추천 5가지 애니메이션 코드
    return render(request, 'animation/detail.html', {'animation': animation, 'is_recommend': is_recommend, 'genre': genre_list})


@login_required
def comment(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # 최신순으로 그 애니에 해당하는 댓글들 가져오기
            animation = Animation.objects.get(id=id)
            comments = Comment.objects.filter(animation=animation).order_by('-created_at')
            # animation_comments = Comment.objects.filter(animation_id=id).order_by('-created_at')

            return render(request, 'animation/detail.html', {'comments': comments})

    elif request.method == "POST":
        my_comment = Comment()
        my_comment.animation = Animation.objects.get(id=id)
        my_comment.animation = request.user
        my_comment.content = request.POST.get('my-content', '')
        my_comment.save()
        return redirect('/detail/' + str(id))

    return redirect('/sign-in')


@login_required
def delete_comment(request, id):
    my_comment = Comment.objects.get(id=id)
    current_ani = my_comment.animation.id
    my_comment.delete()
    return redirect('/detail/' + str(current_ani))


# def bookmark(request, id):
#     animation = Animation.objects.get(id=id)
#     if animation in user.bookmark.all():
#         user.bookmark.remove(animation)
#     else:
#         user.bookmark.add(animation)
#     return redirect('/detail/' + str(id))



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
