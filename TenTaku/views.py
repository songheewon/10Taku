from django.shortcuts import render

def main_view(request):
    return render(request, 'animation/mainpage.html')

def detail_view(request):
    return render(request, 'animation/detail.html')


def select_genre(request):
    return render(request, 'animation/select_genre.html')

def genre_view(request):
    return render(request, 'animation/genrepage.html')

def bookmark_view(request):
    return render(request, 'animation/bookmark.html')

def my_rec_view(request):
    return render(request, 'animation/my_recommend.html')

def search_view(request):
    return render(request, 'animation/search_result.html')

def sign_up_view(request):
    return render(request, 'user/sign_up.html')

def login_view(request):
<<<<<<< HEAD
    return render(request, 'user/login.html')
=======
    return render(request, 'user/login.html')

>>>>>>> develop
