from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

from .models import Client
from accts.models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('id', 'last_payment', 'balance', 'is_current',)

    def __init__(self, *args, **kwargs):
        try:
            client = kwargs.pop('client')
            self.base_fields['owner'].widget = forms.HiddenInput()
        except:
            pass 
        super(AccountForm, self).__init__(*args, **kwargs)



class ClientForm(forms.ModelForm):

    class Meta:
        model = Client 
        exclude = ('id', )