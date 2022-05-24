from django.shortcuts import render

# testing navbar + base.html


def homepage(request):
    return render(request, 'planty/base.html')
