#POSTS go here I think
from django import forms

class Nameform(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)