from django.shortcuts import render

def main_view(request):
    return render(request, 'animation/mainpage.html')

def genre_view(request):
    return render(request, 'animation/genrepage.html')





