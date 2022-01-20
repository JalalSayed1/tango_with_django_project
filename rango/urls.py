from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    # empty string URL will be passed from tango_with_django project if URL included rango/
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
