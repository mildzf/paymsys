from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
import weasyprint
from django.contrib import messages

from .models import  Invoice

import datetime
from django.urls import reverse_lazy
from django.views.generic import FormView
from clients.models import Client
from .forms import InvoiceForm


class BillView(FormView):
    template_name = 'billing/invoice_form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Get all clients
        clients = Client.objects.all()
        # Create a bill for each client with the specified date
        for client in clients:
            invoice = Invoice.objects.create(
                client=client,
                date=datetime.date.today(),
                amount=client.get_total_balance(),
            )
            context = {'invoice': invoice}
            html_template = get_template('billing/invoice_detail.html').render(context)
            pdf_file = weasyprint.HTML(string=html_template).write_pdf()
            email_body = f"Dear {invoice.client},\n\nPlease find attached your invoice for {invoice.date}.\n\nThank you for your business!\n\nBest regards,\n\nMetrocordCuts"
            email = EmailMessage(
                'Invoice',
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [invoice.client.email],
            )
            email.attach('invoice.pdf', pdf_file, 'application/pdf')
            email.send()
        messages.success(self.request, "All Clients have been successfully billed")
        return super().form_valid(form)


