from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm


def index(request):
    # Query the database for a list of ALL categories currently stored. # Order the categories by the number of likes in descending order. # Retrieve the top 5 only -- or all if less than 5. # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    
    # - sign means from top to bottom:
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    
    top_pages = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = top_pages
    
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about'>About</a>")
    # context_dict = {'boldmessage': ' Crunchy, creamy, cookie, candy, cupcake!'}

    # return a rendered response to send to the client:
    # NB: the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context= context_dict)


def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Can we find a category name slug with the given name? # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages. # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages:
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category. # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided a valid form:
        if form.is_valid():
            # save the new category to the database:
            form.save(commit=True)
            # now we can confirm that the category is saved or not.
            # but for now, just redirect:
            return redirect('/rango/')

        else:
            # if supplied form contained errors:
            print(form.errors)
    
    # we will handle the bad form, new form, or no form supplied cases
    # render the form with error messages, if any:
    return render(request, 'rango/add_category.html', {'form':form})
            
            
def add_page(request):
    try:
        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect('/rango/')

        
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                # returns the object if saved:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                # redirect user to show_category is page was created:
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)



    