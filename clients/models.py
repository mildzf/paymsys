from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('last_name', 'first_name',)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('clients:delete', kwargs={'pk':self.pk})

    def get_update_url(self):
        return reverse('clients:update', kwargs={'pk':self.pk})

    def get_create_url(self):
        return reverse('clients:create', kwargs={'pk':self.pk})

