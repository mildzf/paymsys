from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Invoice 



class InvoiceDetailView(DetailView):
    model = Invoice
    context_object_name = "invoice"
    template_name = "billing/invoice_detail.html"

