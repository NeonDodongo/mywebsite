from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':5,
                'placeholder': 'Tell me all about it.'
            }
        ), 
        max_length=4000,
        help_text='Max length is 4000 characters.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']