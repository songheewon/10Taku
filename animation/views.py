from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def my_recommend_view(request):


    return render(request, 'animation/my_recommend.html')
