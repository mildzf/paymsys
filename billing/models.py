from django.db import models
from django.urls import reverse
from clients.models import Client
from accts.models import Account


class Invoice(models.Model):
    client = models.ForeignKey(Client, related_name="invoices", on_delete=models.CASCADE, blank=True, null=True)
    items = models.ForeignKey(Account, related_name="item_invoices", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"Bill for {self.date}"

    def get_absolute_url(self):
        return reverse("billing:detail", kwargs={'pk':self.pk})
