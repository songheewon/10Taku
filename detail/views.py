from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Bookmark
from animation.models import Animation
from user.models import UserModel

# Create your views here.
def show_detail_view(request):
    return render(request, 'animation/detail.html')


@login_required
def comment(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            #최신순으로 그 애니에 해당하는 댓글들 가져오기
            animation = Animation.objects.get(id=id)
            comments = Comment.objects.filter(animation=animation).order_by('-created_at')

            return render(request, 'detail/detail.html', {'comments': comments})

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
    return redirect('/detail/'+str(current_ani))


# def bookmark(request, id):
#     animation = Animation.objects.get(id=id)
#     if animation in user.bookmark.all():
#         user.bookmark.remove(animation)
#     else:
#         user.bookmark.add(animation)
#     return redirect('/detail/' + str(id))

