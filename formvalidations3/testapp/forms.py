from django import forms
import re
from django.core import validators

def password_validator(value):
        if (len(value) < 6 ):
            raise forms.ValidationError('password length should be 6')
        elif not re.search("[a-z]", value):
            raise forms.ValidationError('password should contain atleast one lowercase letter')
        elif not re.search("[0-9]", value):
            raise forms.ValidationError('password should contain atleast one digit letter')
        elif not re.search("[A-Z]", value):
            raise forms.ValidationError('password should contain atleast one Upper Case letter')
        elif not re.search("[_$#@!%&^*]", value):
            raise forms.ValidationError('password should contain atleast one Special Character')


class SignUpForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) #password = forms.CharField(widget=forms.PasswordInput,validators=[password_validator])
    rpassword = forms.CharField(widget=forms.PasswordInput,label="Re Enter Password")
    bot_handler = forms.CharField(required=False,widget=forms.HiddenInput)


    def clean(self):
        total_cleaned_data = super().clean()
        pwd = total_cleaned_data['password']
        rpwd = total_cleaned_data['rpassword']
        if (len(pwd) < 6 ):
            raise forms.ValidationError('password length should be 6')
        elif not re.search("[a-z]", pwd):
            raise forms.ValidationError('password should contain atleast one lowercase letter')
        elif not re.search("[0-9]", pwd):
            raise forms.ValidationError('password should contain atleast one digit letter')
        elif not re.search("[A-Z]", pwd):
            raise forms.ValidationError('password should contain atleast one Upper Case letter')
        elif not re.search("[_$#@!%&^*]", pwd):
            raise forms.ValidationError('password should contain atleast one Special Character')

        if pwd != rpwd:
            raise forms.ValidationError('password not matching')
        bot_handler_value = total_cleaned_data['bot_handler']
        if len(bot_handler_value)>0:
            raise forms.ValidationError('Request from BOT can not be subbmitted')
