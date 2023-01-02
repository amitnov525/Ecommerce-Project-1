from django import forms 
from store_app.models import ReviewRating

class MyForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']