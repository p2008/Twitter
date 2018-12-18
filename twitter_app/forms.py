from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class AddTweetForm(forms.Form):
    content = forms.CharField(label='', max_length=140,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Nowy wpis'}))


class AddCommentForm(forms.Form):
    content = forms.CharField(label='', max_length=60,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Nowy komentarz'}))


class AddMessageForm(forms.Form):
    content = forms.CharField(label='',
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Nowa wiadomość'}))


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
