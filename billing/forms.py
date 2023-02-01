from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

from .models import Invoice  



class InvoiceForm(forms.ModelForm):
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
        )
    )
    due_date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)   
  

    class Meta:
        model = Invoice 
        exclude = ['id',]

    
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['date'].help_text = "The billing date"
        self.fields['date'].label = "Billing Date"
        self.fields['due_date'].help_text = "Payment due by this date"
        self.fields['due_date'].label = "Due Date"
        self.base_fields['client'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.form_id = 'billingForm'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('date',  css_class="form-control border border-dark border-2 border-0 border-bottom " ),
                Field('due_date',  css_class="form-control border border-dark border-2 border-0 border-bottom mt-3")
                ),
            Submit('submit', 'Bill Client', css_class='btn btn-success mt-4'),
        )