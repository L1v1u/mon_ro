from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from projects.models import Loc
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data


class UserProfileForm(forms.Form):
    firstname = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': _('Firstname'), 'class': 'form-control'})
    )

    lastname = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': _('Lastname'), 'class': 'form-control'})
    )

    address_1 = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'placeholder': _('address 1'), 'class': 'form-control'})
    )

    address_2 = forms.CharField(
        required=False,
        widget=forms.TextInput( attrs={'placeholder': _('address 2'), 'class': 'form-control'})
    )

    address_city = forms.ModelChoiceField(
        label=_('Address city:'),
        queryset=Loc.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete_locs', attrs={'class': 'form-control'})
    )

    phonenumber =  forms.RegexField('^(\+4|)?(07[0-8]{1}[0-9]{1}|02[0-9]{2}|03[0-9]{2}){1}?(\s|\.|\-)?([0-9]{3}(\s|\.|\-|)){2}$',
        widget=forms.TextInput(attrs={'placeholder': _('phone number'), 'class': 'form-control'})
    )

    subscription_sms_alerts = forms.BooleanField(required=False, label='subscribe to sms alerts')
    subscription_newsletter = forms.BooleanField(required=False, label='subscribe to newsletter')
    subscription_surveys = forms.BooleanField(required=False, label='subscribe to surveys')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(Row(
                Column('firstname', css_class='col-md-6'),
                Column('lastname', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('address_1', css_class='col-md-6'),
                Column('address_2', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('address_city', css_class='col-md-6'),
                Column('phonenumber', css_class='col-md-6'),
                css_class='form-group'
            ),
            Row(
                Column('subscription_sms_alerts', css_class='col-md-12'),

                css_class='form-group'
            ),
            Row(
                Column('subscription_newsletter', css_class='col-md-12'),

                css_class='form-group'
            ),
            Row(

                Column('subscription_surveys', css_class='col-md-12'),
                css_class='form-group'
            ),
            Submit('submit', _('Save')))


