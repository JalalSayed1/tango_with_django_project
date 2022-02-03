from unittest.util import _MAX_LENGTH
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True) # CharField to store chars (eg. strings), args are optional
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True) # blank=True to make it unimportant field to be completed in the admin interface
    NAME_MAX_LENGTH  = 128

    # overriding save func:
    def save(self, *args, **kwargs):
        # "why not" => "why-not":
        self.slug = slugify(self.name)
        # call parent save() func:
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Page(models.Model):
    
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    
    # ForeignKey means OneToMany relationship, CASCADE means deleting it will delete the pages associated with it
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
