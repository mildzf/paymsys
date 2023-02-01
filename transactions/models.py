from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _

from accts.models import Account


class Transaction(models.Model):
    class Payment(models.TextChoices):
        CSH = "CSH", _("Cash")
        CRD = "CRD", _("Credit/Debit Card")
        PPL = "PPL", _("PayPal")
        TRN = "TRN", _("Bank Transfer")
        OTH = "OTH", _("Other")
    payment = models.CharField(max_length=3, choices=Payment.choices, default=Payment.CSH)
    account = models.ForeignKey(Account, related_name="transactions", on_delete=models.CASCADE)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"{self.account.id}"

    def get_absolute_url(self):
        return reverse('transactions:detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('transactions:create')

    def get_receipt(self):
        return reverse("transactions:receipt", kwargs={'pk':self.pk})


class Receipt(models.Model):
    transaction = models.OneToOneField(Transaction, related_name="receipt", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"{self.id:'04d'}"

    

