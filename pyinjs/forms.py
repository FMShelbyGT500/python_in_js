from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {'content': ''}


class SimpleForm(forms.Form):
    post = forms.CharField()
