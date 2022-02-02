import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # first we will create lists of dictionaries containing the pages
    # we want to add into each category
    # then might seem a little bit confusing but it allows us iterate through each data structure and add the data to our models
    
    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'views':10},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'views':5},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'views':7}
    ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views':11},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views':12},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views':13}
    ]
    
    other_page = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views':14},
        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views':15}
    ]
    
    cats = {'Python' : {'pages' : python_pages,
            'views' : 128,
            'likes' : 64},

            'Django' : {'pages' : django_pages,
            'views' : 64,
            'likes' : 32},

            'Other Frameworks' : {'pages' : other_page,
            'views' : 32,
            'likes' : 16}
            }

    #! if want to add more categories or pages, add them to the dicts above.

    # to go through the cats dict then adds each category and then adds all the associated pages for that category
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

def add_page(cat, title, url, views=0):
    # get_or_create returns a tuple (object, boolean); object is reference to model instance that it creates, boolean true if created successfully
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
    
    
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
        
    
