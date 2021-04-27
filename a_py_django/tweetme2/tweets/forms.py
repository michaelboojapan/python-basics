from django import forms
from .models import Tweet

# Create your models here.

from django.conf import settings
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(forms.ModelForm):

    # content = forms.CharField(required=False,
    #                               widget=forms.Textarea(
    #                                   attrs={
    #                                       'class': 'new-class-name two',
    #                                       'rows': 10,
    #                                       'cols': 120,
    #                                       'id': 'my-id-for-textarea',
    #                                   }
    #                               )
    #                          )

    class Meta:
        model = Tweet
        fields = [
            'content',
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError('this tweet is too long')
        return content




