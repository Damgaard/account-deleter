from django.shortcuts import render


def index(request):
    context = {'hey': 5}
    return render(request, 'undo/index.html', context)
