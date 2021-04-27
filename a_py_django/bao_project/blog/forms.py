from django import forms
from .models import Article

# Create your models here.

class ArticleForm(forms.ModelForm):

    title = forms.CharField(required=True, label='title',
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'blog title'
                                }
                            ))

    content = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={
                                          'class': 'new-class-name',
                                          'rows': 15,
                                          'cols': 120,
                                      }
                                  )
                             )
    author = forms.CharField(required=False, label='author',
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'your name'
                                }
                            ))

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'author'
        ]




