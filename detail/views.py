from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Bookmark, Recommend
from animation.models import Animation, Genre

# Create your views here.
def show_detail_view(request):
    return render(request, 'animation/detail.html')


# @login_required
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

    is_bookmarked = Bookmark.objects.filter(user=user, animation=animation).exists()
    is_recommended = Recommend.objects.filter(user=user, animation=animation).exists()
    comments = Comment.objects.filter(animation=animation).order_by('-created_at')

    #컨텐츠 기반 장르 5가지 추천 코드
    #협업필터링 유저추천 5가지 애니메이션 코드
    return render(request, 'animation/detail.html', {
        'animation': animation,
        'genre': genre_list,
        'is_bookmarked': is_bookmarked,
        'is_recommended': is_recommended,
        'comments': comments
    })


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


@login_required
def delete_comment(request, id):
    my_comment = Comment.objects.get(id=id)
    current_ani = my_comment.animation.id
    my_comment.delete()
    return redirect('/detail/' + str(current_ani))

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


@login_required
def recommend(request, id):
    user = request.user
    animation = Animation.objects.get(id=id)

    try:
        my_recommend = Recommend.objects.get(user=user, animation=animation)
        my_recommend.delete()
    except Recommend.DoesNotExist:
        my_recommend = Recommend(user=user, animation=animation)
        my_recommend.save()
        return redirect('/detail/' + str(id))
    return redirect('/detail/' + str(id))
