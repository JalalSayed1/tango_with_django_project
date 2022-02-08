from django.urls import path, include
from rango import views

app_name = 'rango'

urlpatterns = [
    # empty string URL will be passed from tango_with_django project if URL included rango/
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    # category_name_slug is the same var name we passed in show_category() in views.py
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    
    path('add_category/', views.add_category, name='add_category'),

    path("category/<slug:category_name_slug>/add_page/", views.add_page, name='add_page'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),
]
