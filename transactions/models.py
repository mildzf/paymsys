from django.db import models
from django.urls import reverse 

from accts.models import Account


class Transaction(models.Model):
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

    

