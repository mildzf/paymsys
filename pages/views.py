from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView
from core.views import StaffViewMixin
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

from clients.models import Client
from accts.models import Account


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class DashboardView(StaffViewMixin, View):
    def get(self, request):
        cards = [
            {'title': 'Search', 'url': reverse('search'), 'icon_class': 'bi bi-search', 'col_size': '4'},
            {'title': 'Make Payment', 'url': reverse('accts:search'), 'icon_class': 'bi bi-credit-card', 'col_size': '4'},
            {'title': 'Accounts', 'url': reverse('accts:list'), 'icon_class': 'bi bi-bank', 'col_size': '4'},
            {'title': 'Transactions', 'url': reverse('transactions:list'), 'icon_class': 'bi bi-calculator', 'col_size': '4'},
            {'title': 'Clients', 'url': reverse('clients:list'), 'icon_class': 'bi bi-people', 'col_size': '4'},
        ]

        if request.user.groups.filter(name='managers').exists():
            cards += [
                {'title': 'Billing', 'url': reverse('billing:create'), 'icon_class': 'bi bi-receipt', 'col_size': '4'},
                {'title': 'Tasks', 'url': reverse('tasks:index'), 'icon_class': 'bi bi-calendar-check', 'col_size': '4'},
            ]

        context = {'cards': cards}
        return render(request, 'pages/home.html', context)



class SearchView(StaffViewMixin, ListView):
    template_name = 'pages/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        client_qs = Client.objects.none()
        account_qs = Account.objects.none()

        if query:
            client_qs = Client.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(address__icontains=query)
            )
            account_qs = Account.objects.filter(
                Q(serial_number__icontains=query) |
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query) |
                Q(owner__email__icontains=query)
            )

        return client_qs, account_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
