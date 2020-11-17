from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Hello World from page index!')

def userinfo(request):
    return HttpResponse('Hello World from page userinfo!')

def baike_content(request):
    return HttpResponse('Hello World from page baike_content!')
