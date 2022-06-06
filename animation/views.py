from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    user = request.user.is_authenticated #유저는 인증된 유저이다.
    if user:
        return redirect('/main') #인증된유저가 있다면
    else:
        return redirect('/login') #인증된 유저가 없다면


@login_required
def my_recommend_view(request):


    return render(request, 'animation/my_recommend.html')
