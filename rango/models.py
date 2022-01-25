from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True) # CharField to store chars (eg. strings), args are optional
    
    def __str__(self):
        return self.name
    
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # ForeignKey means OneToMany relationship, CASCADE means deleting it will delete the pages associated with it
    titile = models.CharField(max_length=128)
    url = models.URLField() # to store URLs
    views = models.IntegerField(default=0) # to store int values
    
    def __str__(self):
        return self.title
    