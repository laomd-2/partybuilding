from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'years': range(2019, 2001, -1)
    }
    return render(request, 'index.html', context=context)
