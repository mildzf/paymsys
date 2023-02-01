from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _

from clients.models import Client


class Invoice(models.Model):    
    client = models.ForeignKey(Client, related_name="invoices", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"Bill for {self.date}"

    def get_absolute_url(self):
        return reverse("billing:detail", kwargs={'pk':self.pk})

    @property
    def get_total(self):
        return sum([acc.balance for acc in self.client.accounts.all()])

    @property
    def get_payable(self):
        return sum([acc.service_fee for acc in self.client.accounts.all()])

