from django import forms

from .models import Post
from .models import Book

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class PostForm_search_with_author(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('author',)

class PostForm_search_with_title(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title',)