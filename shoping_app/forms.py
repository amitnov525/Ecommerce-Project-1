from django import forms

# Create your forms here.

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50,widget= forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length = 50,widget= forms.TextInput(attrs={'class':'form-control'}))
	email_address = forms.EmailField(max_length = 150, widget= forms.EmailInput(attrs={'class':'form-control'}))
	message = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control'}), max_length =200)
