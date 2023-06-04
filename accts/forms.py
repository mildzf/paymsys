from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

from .models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('id', 'last_payment', 'is_current',)


