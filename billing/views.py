from django.core.mail import get_connection, EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import InvoiceForm 
from .models import Invoice 

from accts.models import Account
from clients.models import Client
from core.views import StaffCreateView


class InvoicingView(StaffCreateView):
    model = Invoice
    context_object_name = "invoice"
    template_name = "billing/invoice_form.html"
    form_class = InvoiceForm
    success_url = reverse_lazy('home')
    success_message = "%(name)s was created successfully"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


    def form_valid(self, form):
        billing_date = form.instance.date 
        due_date = form.instance.due_date 
        clients = Client.objects.all()
        template = get_template('billing/emails.html')
        context = super().get_context_data()
        context['billing_date']  = billing_date
        context['due_date'] = due_date
        html_string = template.render(context)
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            for client in clients:
                context['client'] = client
                context['billing_date']  = billing_date
                context['due_date'] = due_date
                html_string = template.render(context)
                recipient_list = [client.email,]
                subject = f"Account Statement for  {billing_date}"
                email_from = settings.EMAIL_HOST_USER
                message = html_string 
                msg = EmailMessage(subject, message, email_from, settings.RECIPIENT_ADDRESS, connection=connection)
                msg.content_subtype = "html"
                msg.send()
            messages.success(self.request, 'Emails sent to clients')
        return super().form_valid(form)


    

