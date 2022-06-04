from django.shortcuts import render

def main_view(request):
    return render(request, 'animation/mainpage.html')

def detail_view(request):
    return render(request, 'animation/detail.html')

def genre_view(request):
    return render(request, 'animation/bookmark.html')

def sign_up_view(request):
    return render(request, 'user/sign_up.html')

def lgoin_view(request):
    return render(request, 'user/login.html')