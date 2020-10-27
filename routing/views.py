from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def simple_route(request):
    return HttpResponse(status=200)


def slug_route(request, slug):
    if slug:
        return HttpResponse(status=200, content=slug)
    else:
        return HttpResponse(status=404)


def sum_route(request, a, b):
    try:
        a = int(a)
        b = int(b)
    except (TypeError, ValueError):
        return HttpResponse(status=404)
    return HttpResponse(status=200, content=a+b)


@require_http_methods(["GET"])
def sum_get_method(request):
    try:
        a = request.GET['a']
        b = request.GET['b']
    except KeyError:
        return HttpResponse(status=400)
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        return HttpResponse(status=400)
    return HttpResponse(status=200, content=a+b)


@require_http_methods(["POST"])
def sum_post_method(request):
    try:
        a = request.POST['a']
        b = request.POST['b']
    except KeyError:
        return HttpResponse(status=400)
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        return HttpResponse(status=400)
    return HttpResponse(status=200, content=a+b)
