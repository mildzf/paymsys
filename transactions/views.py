from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.conf import settings 

from .forms import TransactionForm
from .models import Transaction, Receipt
from accts.models import Account
from core.mixins import PageLinksMixin


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction 


class TransactionListView(LoginRequiredMixin, PageLinksMixin, ListView):
    model = Transaction 
    template_name = "transactions/transaction_list.html"
    paginate_by = settings.PAGINATE_BY
    context_object_name = "transactions"


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction 
    form_class = TransactionForm

    def get_success_url(self):
        return reverse('transactions:detail', kwargs={'pk':self.object.id})

    def get_initial(self):
        initial = super().get_initial()
        acc_no = self.request.GET.get('q', None)
        if acc_no:
            account = get_object_or_404(Account, pk=acc_no)
            initial['account'] = account.id 
            initial['balance_before'] = account.balance
        return initial
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        acc_no = self.kwargs.get('pk', None)
        if acc_no:
            account = get_object_or_404(Account, pk=pk)
            context['account'] = account 
        return context

    def form_valid(self, form):
        account = form.instance.account 
        print("Account: ", account)
        balance_before = account.balance 
        form.instance.balance_before = balance_before
        form.instance.balance_after = balance_before - form.instance.amount 
        account.balance = form.instance.balance_after
        account.save()
        form.instance.save()
        return super().form_valid(form)


class TransactionReceiptView(LoginRequiredMixin, DetailView):
    model = Receipt
    context_object_name = "receipt"
    template_name = "transactions/receipt.html"

    def get_object(self):
        acc_no = self.kwargs.get('pk', None)
        if acc_no:
            transaction = get_object_or_404(Transaction, pk=acc_no)
            receipt, created = Receipt.objects.get_or_create(transaction=transaction)
            return transaction.receipt
        return []