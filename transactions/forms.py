from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FieldWithButtons

from .models import Transaction 
from accts.models import Account 


class TransactionForm(forms.ModelForm):
    account = forms.ModelChoiceField(label="", queryset=Account.objects.all(), empty_label="Choose Account: ")

    class Meta:
        model = Transaction
        fields = [ 'account', 'payment', 'amount']

    def __init__(self, *args, **kwargs):
        self.base_fields['account'].widget = forms.HiddenInput()
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'paymentForm'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('account', css_class="form-control mb-3"),
                Field('payment', style="max-width: 100px", placeholder="Payment type", css_class="form-control mb-3 border border-dark border-2 border-0 border-bottom"),
                'balance_before',
                Field('amount', label='', placeholder='Enter payment amount', css_class="mb-4 border border-dark border-2  border-0 border-bottom border-radius"),
            ),
            Submit('submit', 'Make Payment', css_class='btn btn-success'),
        )