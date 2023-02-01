from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse 

from .forms import InvoiceForm
from .models import Invoice 
from clients.models import Client



class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    context_object_name = "invoice"
    template_name = "billing/invoice_detail.html"


def send_invoices(request):
    context = {
        'clients': Client.objects.all()

    }
    return render(request, "billing/invoice_form.html", context)
    

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice 
    form_class = InvoiceForm

    
    def get_success_url(self):
        return reverse('billing:detail', kwargs={'pk':self.object.id})

    def get_initial(self):
        initial = super().get_initial()
        acc_no = self.kwargs.get('pk', None)
        if acc_no:
            client = get_object_or_404(Client, pk=acc_no)
            initial['client'] = client.id
        return initial
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs.get('pk', None)
        if pk:
            client = get_object_or_404(Client, pk=pk)
            context['client'] = client
        context['clients'] = Client.objects.all()
        return context



from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
import tempfile
import os
from django.conf import settings
from django.core.mail import EmailMessage


def send_pdf(request, **kwargs):
    pk = kwargs.get('pk')
    client = Client.objects.get(pk=pk)
    context = {
        'client': client,
        'image_path':'file://' + os.path.join(settings.STATIC_ROOT, 'images', 'logo.jpeg' )
    }
    html_template = get_template(
        'transactions/receipt.html')
    html_string = html_template.render(context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename=invoice.pdf'
    from_email = 'arycloud7@icloud.com'
    to_emails = [f"{client.email}"]
    subject = "Your bill is ready for viewing"
    message = 'Good day,\n your bill is attached.'
    email = EmailMessage(subject, body=pdf_file, from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach("invoice.pdf", pdf_file, "application/pdf")
    email.content_subtype = "pdf"  # Main content is now text/html
    email.encoding = 'ISO-8859-1'
    email.send()
    return HttpResponse(pdf_file, content_type='application/pdf')


from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def sendHTMLEmail(request, **kwargs):
    pk = kwargs.get('pk')
    client = Client.objects.get(pk=pk)
    context = {
        'client': client,
        'image_path':'file://' + os.path.join(settings.STATIC_ROOT, 'images', 'logo.jpeg' )
    }
    html_content = render_to_string("emails.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "Test HTML Email",
        text_content,
        settings.EMAIL_HOST_USER ,
        ['testemail@gmail.com']
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return HttpResponse("Email Sent successfully")



class TransactionReceiptView(StaffDetailView):
    model = Receipt
    context_object_name = "receipt"
    template_name = "transactions/receipt.html"

    def get_object(self):
        acc_no = self.kwargs.get('pk', None)
        if acc_no:
            transaction = get_object_or_404(Transaction, pk=acc_no)
            receipt, created = Receipt.objects.get_or_create(transaction=transaction)
            return transaction.receipt
        return []