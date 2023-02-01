import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration
from django.contrib import messages

from accts.models import Account
from core.views import StaffCreateView, StaffDetailView, StaffListView

from .forms import TransactionForm
from .models import Receipt, Transaction


class TransactionDetailView(StaffDetailView):
    model = Transaction 


class TransactionListView(StaffListView):
    model = Transaction 
    template_name = "transactions/transaction_list.html"
    paginate_by = settings.PAGINATE_BY
    context_object_name = "transactions"


class TransactionCreateView(StaffCreateView):
    model = Transaction 
    form_class = TransactionForm
    success_message = "Payment successful!"

    def get_success_url(self):
        return reverse('transactions:detail', kwargs={'pk':self.object.id})

    def get_initial(self):
        initial = super().get_initial()
        acc_no = self.request.GET.get('q', None)
        if acc_no:
            account = get_object_or_404(Account, pk=acc_no)
            initial['account'] = account.id 
            initial['balance_before'] = account.balance
        return initial
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        acc_no = self.request.GET.get('q', None)
        if acc_no:
            account = get_object_or_404(Account, pk=acc_no)
            context['account'] = account 
        return context

    def form_valid(self, form):
        account = form.instance.account 
        balance_before = account.balance 
        form.instance.balance_before = balance_before
        form.instance.balance_after = balance_before - form.instance.amount 
        account.balance = form.instance.balance_after
        account.save()
        form.instance.save()
        return super().form_valid(form)


def receipt(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    # queryset
    receipt = Receipt.objects.get_or_create(transaction=transaction)[0]
    # context passed in the template
    context = {
        "receipt": receipt,
        "image_path": 'file://' + os.path.join(settings.STATIC_ROOT, 'images', 'logo.jpeg' )}

    # render
    font_config = FontConfiguration()
    template = get_template(
        'transactions/receipt.html')
    html_string = template.render(context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf(stylesheets=[CSS(string='body { font-family: serif !important }')])

    # http response
    response = HttpResponse(pdf_file, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=receipt.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    return response