from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.conf import settings 

from .forms import ClientForm
from .models import Client
from core.views import (StaffListView, StaffCreateView, 
StaffDeleteView, StaffDetailListView, StaffUpdateView)


class ClientListView(StaffListView):
    model = Client
    context_object_name = "clients"
    paginate_by = settings.PAGINATE_BY



class ClientDetailView(StaffDetailListView):
    paginate_by = 10 
    template_name = 'clients/client_detail.html'
    paginate_by = settings.PAGINATE_BY

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Client.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.object 
        return context 

    def get_queryset(self):
        return self.object.accounts.all()


class ClientCreateView(StaffCreateView):
    model = Client 
    form_class = ClientForm 

    def get_success_url(self):
        return reverse("clients:detail", kwargs={'pk': self.object.id})


class ClientUpdateView(StaffUpdateView):
    model = Client 
    form_class = ClientForm 
    template_name = "clients/client_update_form.html"

    def get_success_url(self):
        return reverse("clients:detail", kwargs={'pk': self.object.id})


class ClientDeleteView(StaffDeleteView):
    model = Client 
    context_object_name = "client"
    success_url = reverse_lazy("clients:list")


