from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return HttpResponse("There gonna be my blog's home page")


def detail(request, pk):
    return HttpResponse("There gonna be article's full text")
