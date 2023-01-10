from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.conf import settings 

from .forms import AccountForm, ClientForm
from .models import Client
from accts.models import Account 
from core.mixins import PageLinksMixin


class ClientListView(LoginRequiredMixin, PageLinksMixin, ListView):
    model = Client
    context_object_name = "clients"
    paginate_by = settings.PAGINATE_BY



class ClientDetailView(LoginRequiredMixin, SingleObjectMixin, PageLinksMixin, ListView):
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


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client 
    form_class = ClientForm 

    def get_success_url(self):
        return reverse("clients:detail", kwargs={'pk': self.object.id})


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client 
    form_class = ClientForm 
    template_name = "clients/client_update_form.html"

    def get_success_url(self):
        return reverse("clients:detail", kwargs={'pk': self.object.id})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client 
    context_object_name = "client"
    success_url = reverse_lazy("clients:list")
