from django import forms
from .models import Product

# Create your models here.

class ProductForm(forms.ModelForm):

    title = forms.CharField(required=True, label='',
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'your title',
                                    'id': 'my-id-for-titled',

                                }
                            ))

    email = forms.EmailField()
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'class': 'new-class-name two',
                                          'rows': 10,
                                          'cols': 120,
                                          'id': 'my-id-for-textarea',
                                      }
                                  )
                             )
    price = forms.DecimalField(initial=199.99)

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if not 'CFE' in title:
            raise forms.ValidationError('CFE not in title')
        if not 'news' in title:
            raise forms.ValidationError('news not in title')
        else:
            return title

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith('edu'):
            raise forms.ValidationError('this is not a valid email')
        return email



class RawProductForm(forms.Form):
    title = forms.CharField(required=True, label='',
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'your title',
                                    'id': 'my-id-for-titled',

                                }
                            ))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'class': 'new-class-name two',
                                          'rows': 10,
                                          'cols': 120,
                                          'id': 'my-id-for-textarea',
                                      }
                                  )
                                  )
    price = forms.DecimalField(initial=199.99)

