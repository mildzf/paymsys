from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.conf import settings 
from django.shortcuts import get_object_or_404 

from .forms import AccountForm
from .models import Account
from clients.models import Client 
from transactions.models import Transaction
from core.mixins import PageLinksMixin


class AccountListView(LoginRequiredMixin, PageLinksMixin, ListView):
    model = Account 
    context_object_name = "accounts"
    paginate_by = settings.PAGINATE_BY


class AccountSearchView(LoginRequiredMixin, PageLinksMixin, ListView):
    model = Account 
    context_object_name = "accounts"
    template_name = "accts/search.html"
    paginate_by = settings.PAGINATE_BY
    
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        accounts = Account.objects.all()
        if query:
            accounts = accounts.filter(
                Q(client__last_name__startswith=query)|
                Q(client__first_name__startswith=query)|
                Q(number__startswith=query)|
                Q(name__startswith=query)
            )
            return accounts   
        return []

class AccountDetailView(LoginRequiredMixin, SingleObjectMixin, PageLinksMixin, ListView):
    paginate_by = 10
    template_name = "accts/account_detail.html"
    paginate_by = settings.PAGINATE_BY

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Account.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = self.object
        return context

    def get_queryset(self):
        return self.object.transactions.all()


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account 
    form_class = AccountForm
    
    def get_success_url(self):
        return reverse('accts:detail', kwargs={'pk':self.object.id})

    def get_initial(self):
        initial = super().get_initial()
        acc_no = self.request.GET.get('q', None)
        if acc_no:
            client = get_object_or_404(Client, pk=acc_no)
            initial['client'] = client.id
        return initial
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        pk = self.request.GET.get('q', None)
        if pk:
            client = get_object_or_404(Client, pk=pk)
            context['client'] = client
        return context

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = "accts/account_update_form.html"
    
    def get_success_url(self):
        return reverse('accts:detail', kwargs={'pk':self.object.id})


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account 
    success_url = reverse_lazy('accts:list')