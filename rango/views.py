from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
            
            
def add_page(request, category_name_slug):
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
                return redirect(reverse('rango:show_category', 
                                        kwargs={'category_name_slug':category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # to tell the template whether the registration was successful:
    registered = False

    # if HTTP POST request, we are interested in processing form data:
    if request.method == 'POST':
        # attempt to grab info from the raw form info
        # NB: we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        # if the 2 forms are valid:
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database
            user = user_form.save()
            
            # hash the password with the set_password method then update the user object:
            user.set_password(user.password)
            user.save()
            
            # since we need to set the user attribute for UserProfile ourselves, set commit to False
            # This delays saving the model until we are ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user # we are only allowed to to this bc commit is False above
            
            # if user provided profile picture, get it from input form and put it in the UserProfile model:
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # save UserProfile model instance:
            profile.save()
            
            # registration was successful:
            registered = True

        else:
            # invalid form or forms, mistakes or somthing else?
            print(user_form.errors, profile_form.errors)
            
    else:
        # no HTTP POST, so we render out form using 2 ModelForm instances
        # these forms will be blank, ready for user input:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'rango/register.html', context={'user_form':user_form,
                                                           'profile_form':profile_form,
                                                           'registered':registered})        

def user_login(request):
    if request.method == 'POST':
        # these info is obtained form the login form
        # request.POST.get('variable') as opposed to request.POST['variable']
        # request.POST.get('variable') returns None if the value does not exist while request.POST['variable'] will raise a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use django's machinery to attempt to see if the username/password combination is valid
        # User object is returned if it is:        
        user = authenticate(username=username, password=password)

        # if we have a User object, the details are correct
        # if None, no user with matching credentails was found:
        if user:
            # is the account active? (it could be disabled)
            if user.is_active:
                # log user in by sending him to homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive account:
                return HttpResponse('Your Rango account is disabled.')
            
        else:
            # bad login details were provided:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        # the request is not not a HTTP POST, so display the login form:
        # no context dictionary to pass to the template
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
     return HttpResponse("Since you're logged in, you can see this text!")
    
@login_required
def user_logout(request):
    # since we know the user is logged in, we can just log them out
    logout(request)
    return redirect(reverse('rango:index'))
    