from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=355,blank=True)
    cat_img=models.ImageField(upload_to='photos/category',blank=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    def __str__(self):
        return self.cat_name
    
    


