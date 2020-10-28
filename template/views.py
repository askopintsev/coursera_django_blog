from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def echo(request):
    method = request.method.lower()
    header = request.META.get('HTTP_X_PRINT_STATEMENT', 'empty')
    if method == 'get':
        params = request.GET.copy()
    elif method == 'post':
        params = request.POST.copy()

    content = {"method": method, "params": params, "statement": header}

    return render(request, 'echo.html', context=content, status=200)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
