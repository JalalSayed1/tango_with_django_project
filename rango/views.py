from django.shortcuts import render
from django.http import HttpResponse
from rango import views

def index(request):
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about'>About</a>")
    context_dict = {'boldmessage': ' Crunchy, creamy, cookie, candy, cupcake!'}
    # return a rendered response to send to the client:
    # NB: the first para is the template we wish to use
    return render(request, 'rango/index.html', context= context_dict)

def about(request):
    return render(request, 'rango/about.html')

