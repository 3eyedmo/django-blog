from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email',]

    def clean_email(self):
        return self.cleaned_data['email']

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data['password1']
        password2 = data['password2']
        if not (password1 and password2):
            raise forms.ValidationError('please fill the password 1 or 2 ..!!!')
        if data['password2'] != data['password2']:
            raise forms.ValidationError('second passworrd is wrong ..!!! **')
        
        return data['password2']

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_admin', 'is_staff']

    def clean_password(self):
        
        return self.initial["password"]


class PasswordResetForm(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("invalid password")

        if len(password2) < 8:
            raise forms.ValidationError("invalid password")

        return password2