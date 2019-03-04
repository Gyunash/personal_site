from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post
from django import forms
from .models import *
from .views import *


''' ПОЛЬЗОВАТЕЛИ '''
class ContactForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body", "tags"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data["slug"].lower()

        if new_slug == "create":
            raise ValidationError("Slug may not be 'create' ...")
        return new_slug


''' Теги для ПОСТ '''

# class TagForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     slug = forms.CharField(max_length=50)

#     def clean_slug(self):
#         new_slug = self.cleaned_data["slug"].lower()

#         if new_slug == 'create':
#             raise ValidationError("not create slug")
#         return new_slug

#     def save(self):
#         new_tag = Tag.objects.create(
#             title=self.cleaned_data["title"],
#             slug=self.cleaned_data["slug"]
#         )
#         return new_tag


class ChatForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text for your message for chat..', 'rows': '2', 'cols': '50'}))
    class Meta:
        model = Chat
        fields = ('message', )


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text for your comment..', 'rows': '2', 'cols': '50'}))
    class Meta:
        model = Comment
        fields = ('content', )


class RoomForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text for your message for chat..', 'rows': '2', 'cols': '50'}))
    class Meta:
        model = MessageChatRoom
        fields = ('content', )

    # def __init__(self, *args, **kwargs):
    #     user_id = kwargs.pop('user_id', None)

    #     super(RoomForm, self).__init__(*args, **kwargs)

    #     self.fields['road'].queryset = Roads.objects.filter(contractor=user_id)