from django import forms
from grouppost.models import PostImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image', )
