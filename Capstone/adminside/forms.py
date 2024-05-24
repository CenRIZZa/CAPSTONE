from django import forms
from userauth.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['lrn', 'fname', 'lname', 'address','birthday','age', 'email',] 
