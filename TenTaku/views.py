from django.shortcuts import render

def main_view(request):
    return render(request, 'animation/mainpage.html')

def detail_view(request):
    return render(request, 'animation/detail.html')