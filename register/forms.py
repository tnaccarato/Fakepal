from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from payapp.models import Account



class UserForm(UserCreationForm):
    """
    Form for creating a new user and account
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        """
        Saves the user and creates an account for the user

        :param commit:
        :return:
        """
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            account = Account(user=user)
            account.save()
        return user


class LoginForm(forms.Form):
    """
    Form for logging in a user
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

