from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    # empty string URL will be passed from tango_with_django project if URL included rango/
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    # category_name_slug is the same var name we passed in show_category() in views.py
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
]
