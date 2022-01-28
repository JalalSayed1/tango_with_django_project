from django.shortcuts import render
from django.http import HttpResponse
from rango import views
from rango.models import Category


def index(request):
    return HttpResponse("Rango says hey there partner! <a href='/rango/about'>About</a>")
def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")

# ! chapter 6:
# def index(request):
#     # Query the database for a list of ALL categories currently stored. # Order the categories by the number of likes in descending order. # Retrieve the top 5 only -- or all if less than 5. # Place the list in our context_dict dictionary (with our boldmessage!)
#     # that will be passed to the template engine.
    
#     category_list = Category.objects.order_by('-likes')[:5]

#     context_dict = {}
#     context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
#     context_dict['categories'] = category_list
    
#     # return HttpResponse("Rango says hey there partner! <a href='/rango/about'>About</a>")
#     # context_dict = {'boldmessage': ' Crunchy, creamy, cookie, candy, cupcake!'}

#     # return a rendered response to send to the client:
#     # NB: the first para is the template we wish to use
#     return render(request, 'rango/index.html', context= context_dict)

# def about(request):
#     return render(request, 'rango/about.html')

