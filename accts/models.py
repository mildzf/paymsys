from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _ 

from clients.models import Client 



class AccountManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Account(models.Model):
    client = models.ForeignKey(Client, related_name="accounts", on_delete=models.CASCADE)
    number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    class TypeChoices(models.TextChoices):
        RCP=  "RCP", _("Recurring payment")
        LAY = "LAY", _("Layaway")
        OTP = "OTP", _("One time payment")
    acc_type = models.CharField(max_length=3, choices=TypeChoices.choices, default=TypeChoices.RCP)
    service_fee = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_payment = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_current = models.BooleanField(default=True)
    objects = AccountManager()

    class Meta:
        ordering = ['-last_payment', ]

    def __str__(self):
        return f"{self.client} - {self.name} - {self.number}"

    def get_absolute_url(self):
        return reverse('accts:detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('accts:delete', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('accts:update', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('accts:create')

    def get_payment_url(self):
        return reverse('transactions:create', kwargs={'pk': self.pk})

    def get_transaction_history(self):
        return reverse('transactions:list', kwargs={'pk': self.pk})

