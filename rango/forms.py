# this file can be put inside models.py but put it separate make the project tidier

from dataclasses import field
from django import forms
from rango.models import Page, Category

class CategoryForm (forms.ModelForm):
    
    max_length = 128
    
    name = forms.CharField(max_length=max_length, help_text="Please enter the category name.")
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

    max_length = 128
    max_length_url = 200
    
    title = forms.CharField(max_length=max_length, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=max_length_url, help_text="Please enter the url of the page.")
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
        url = cleaned_data.get(url)

        # if url is not empty and does not start with http:// then we append it:
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['utl'] = url

        return cleaned_data
    


