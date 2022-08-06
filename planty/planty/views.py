from django.shortcuts import render
from posts.models import Post


def homepage(request):
    posts = Post.objects.all().order_by('-date_posted')[:9]
    return render(request, 'planty/homepage.html', {'posts': posts})
