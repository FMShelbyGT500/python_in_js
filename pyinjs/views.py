from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse()

def post_list(request):
    return render(request, 'pyinjs/post_list.html', {})

# Create your views here.
# def post_list(request):
#     return render(request, 'templates/post_list.html')
