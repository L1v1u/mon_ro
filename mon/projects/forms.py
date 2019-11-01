from django import forms
from traders.models import TraderType
from projects.models import Loc
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _


class CreateProjectForm(forms.Form):

    trader = forms.ModelChoiceField(
        label=_('Trader:'),
        queryset=TraderType.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete_tradertype', attrs={'class': 'form-control'})
    )
    loc = forms.ModelChoiceField(
        label=_('Location:'),
        queryset=Loc.objects.all(),
        widget=autocomplete.ModelSelect2(url='autocomplete_locs', attrs={'class': 'form-control'})
    )
    #
    #
    name_project = forms.CharField(
        min_length=10,
        label=_('Name Project'),
        widget=forms.TextInput(attrs={'placeholder': _('name project'), 'class': 'form-control'} )
    )
    descr_project = forms.CharField(
        min_length=100,
        label=_('Description:'),

        widget=forms.Textarea(attrs={'placeholder': _('Project description'),  'class':'form-control'})
    )
    terms_and_conditions = forms.BooleanField(required=True, label='Accept terms and conditions')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        if not self.user.is_authenticated:
            self.fields["email"] = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': _('Email'), 'class': 'form-control'}))
            self.fields["password"] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

        self.helper.layout = Layout(Row(
                Column('trader', css_class='col-md-12'),
                css_class='form-group'
            ),
            Row(
                Column('loc', css_class='col-md-12'),
                css_class='form-group'
            ),
            Row(
                Column('name_project', css_class='col-md-12 mb-0'),
                css_class='form-group'
            ),
            Row(
                Column('descr_project', css_class='form-group col-md-12 mb-0'),
                css_class='form-group'
            ),

            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-group'
            ) if not self.user.is_authenticated else Row(),
            Row(
                Column('terms_and_conditions', css_class='form-group col-md-12 mb-0'),
                css_class='form-group'
            ),
            Submit('submit', _('Publish project')))



