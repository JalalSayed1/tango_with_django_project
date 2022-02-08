# this file can be put inside models.py but put it separate make the project tidier

from django import forms
from tango_with_django_project.rango.models import UserProfile
from rango.models import Category, Page
from django.contrib.auth.models import User
from rango.models import UserProfile


class CategoryForm (forms.ModelForm): 
    
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH , help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # an inline class to provide additional info on the form:
    class Meta:
        # provide an association between the ModelForm and model:
        model = Category
        # fields to define what attributes to include:
        fields = ('name',)

class PageForm(forms.ModelForm):
    
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH , help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the url of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # What fields do we want to include in our form? # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them. # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        # or specify the fields to include (don't include the category field). #fields = ('title', 'url', 'views')
        exclude = ('category',)
        
    # override clean():
    def clean(self):
        # a dict:
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # if url is not empty and does not start with http:// then we append it:
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['utl'] = url

        return cleaned_data
    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


