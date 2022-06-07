from django.shortcuts import render

def main_view(request):
    return render(request, 'animation/mainpage.html')

def select_genre(request):
    return render(request, 'user/select_genre.html')

def genre_view(request):
    return render(request, 'animation/genrepage.html')





