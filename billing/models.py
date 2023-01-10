from django.db import models
from django.urls import reverse 

from clients.models import Client 


class Invoice(models.Model):
    client = models.ForeignKey(Client, related_name="invoices", on_delete=models.CASCADE)
    billing_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', '-billing_date',)

    def __str__(self):
        return f"{self.id|stringformat:'05d'}"

    def get_absolute_url(self):
        return reverse("billing:detail", kwargs={'pk':self.pk})

    @property
    def get_total(self):
        return sum([acc.balance for acc in self.client.accounts.all()])

    @property
    def get_payable(self):
        return sum([acc.service_fee for acc in self.client.accounts.all()])

