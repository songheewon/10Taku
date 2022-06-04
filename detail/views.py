from django.shortcuts import render

def show_detail_view(request):
    return render(request, 'animation/detail.html')
