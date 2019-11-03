from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class TradesmanForm(forms.Form):

    firstname = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': _('Firstname'), 'class': 'form-control'})
    )

    lastname = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': _('Lastname'), 'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Email'), 'class': 'form-control'})
    )

    phone_number =  forms.RegexField('^(\+4|)?(07[0-8]{1}[0-9]{1}|02[0-9]{2}|03[0-9]{2}){1}?(\s|\.|\-)?([0-9]{3}(\s|\.|\-|)){2}$',
        widget=forms.TextInput(attrs={'placeholder': _('phone number'), 'class': 'form-control'})
    )

    username = forms.CharField( min_length=5,
        widget=forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    accept_terms_and_conditions = forms.BooleanField(required=True, label='I have read and understood '
                                                                          'Terms and conditions,the privacy '
                                                                          'notice and cookie policy.')

    subscription_newsletter = forms.BooleanField(required=False, label='subscribe to newsletter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(Row(
                Column('firstname', css_class='col-md-6'),
                Column('lastname', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone_number', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('username', css_class='col-md-6'),
                Column('password', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('accept_terms_and_conditions', css_class='col-md-12'),

                css_class='form-group'
            ),
            Row(
                Column('subscription_newsletter', css_class='col-md-12'),

                css_class='form-group'
            ),
            Submit('submit', _('Save')))

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=data.lower())
            if user:
                raise forms.ValidationError("Email already used!")
        except CustomUser.DoesNotExist:
            return data

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = CustomUser.objects.get(username=data.lower())
            if user:
                raise forms.ValidationError("Username already used!")
        except CustomUser.DoesNotExist:
            return data
