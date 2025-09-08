from django.shortcuts import render, HttpResponse


def text_view(request):
    return HttpResponse("Текстовый ответ!")


def template_view(request):
    return render(request, "base.html")