from django import forms
from .models import Task
from blog.models import Post


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["author","title"]
        widgets = {
            "author": forms.HiddenInput(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'image',
            'title',
            'content',
            'tags',
            'category',
            'status',
            'login_require',
            
        ]
        # widgets = {
        #     "author": forms.HiddenInput(),
        # }