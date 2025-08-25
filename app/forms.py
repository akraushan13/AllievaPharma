from itertools import product

from django import forms
from django.forms import ModelForm
from unicodedata import category

from .models import Product, ProductImage, Application


class ProductForm(ModelForm):
  class Meta:
    model = Product
    fields = ['name', 'brand_name', 'composition', 'manufacture', 'form','country_of_origin','packing', 'category', 'subcategory', 'descriptions', 'uses', 'side_effects', 'dosage' ]
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
      'composition': forms.TextInput(attrs={'class': 'form-control'}),
      'manufacture': forms.TextInput(attrs={'class': 'form-control'}),
      'form': forms.TextInput(attrs={'class': 'form-control'}),
      'country_of_origin': forms.TextInput(attrs={'class': 'form-control'}),
      'packing': forms.TextInput(attrs={'class': 'form-control'}),
      'category': forms.TextInput(attrs={'class': 'form-control'}),
      'subcategory': forms.TextInput(attrs={'class': 'form-control'}),
      'descriptions': forms.TextInput(attrs={'class': 'form-control'}),
      'uses': forms.TextInput(attrs={'class': 'form-control'}),
      'side_effects': forms.TextInput(attrs={'class': 'form-control'}),
      'dosage': forms.TextInput(attrs={'class': 'form-control'})
    }
  
  class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
  
class MultipleFileInput(forms.ClearableFileInput):
  allow_multiple_selected = True

class MultipleFileField(forms.FileField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("widget", MultipleFileInput())
    super().__init__(*args, **kwargs)
  
  def clean(self, data, initial=None):
    single_file_clean = super().clean
    if isinstance(data, (list, tuple)):
      result = [single_file_clean(d, initial) for d in data]
    else:
      result = single_file_clean(data, initial)
    return result


class ProductImageForm(ModelForm):
  images = MultipleFileField(label='Select files', required=False)
  
  class Meta:
    model = ProductImage
    fields = ['images']
    widgets = {
      'images': MultipleFileInput(attrs={'multiple': True})
    }


class ApplicationForm(forms.ModelForm):
  consent = forms.BooleanField(required=True, label="I consent to Allieva Pharma processing my personal data")
  
  class Meta:
    model = Application
    fields = ["job", "first_name", "last_name", "email", "phone", "resume", "cover_letter", "consent"]
    
    widgets = {
      "job": forms.HiddenInput(),  # hidden job field
      "cover_letter": forms.Textarea(attrs={ "placeholder": "Tell us why you're the right candidate...", "rows": 5}),
    }