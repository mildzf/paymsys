from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _ 

from clients.models import Client 



class AccountManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Account(models.Model):
    owner = models.ForeignKey(Client, related_name="accounts", null=True, on_delete=models.SET_NULL)
    serial_number = models.CharField(max_length=50)
    class ModelChoices(models.TextChoices):
        LTE = "LTE", _("FireTV Stick Lite")
        REG = "REG", _("FireTV Stick")
        F4K = "F4K", _("FireTV Stick 4K")
        MAX = "MAX", _("FireTV Stick 4k Max")
        CUB = "CUB", _("FireTV Cube")
        OMN = "OMN", _("FireTV Omni Series Smart TV")
        OTH = "OTH", _("Other device")
    model = models.CharField(max_length=3, choices=ModelChoices.choices, default=ModelChoices.REG)
    service_fee = models.DecimalField(max_digits=6, decimal_places=2)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    last_payment = models.DateField(blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = AccountManager()

    class Meta:
        ordering = ('-last_payment',)
        verbose_name = "FireTV Account"

    def __str__(self):
        return f"{self.get_model_display()}"

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




    

