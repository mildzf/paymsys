from django.urls import path
from django.views.generic import TemplateView

from .views import (charge_accounts, save_database_view, save_accts_csv_view,
save_clients_csv_view, save_transactions_csv_view)


app_name="tasks"

urlpatterns = [
    path("all/", TemplateView.as_view(template_name="tasks/index.html"), name="index"),
    path("charge/", charge_accounts, name="charge"),
    path("save-database/", save_database_view, name="database-save"),
    path("download-accts/", save_accts_csv_view, name="accts-save"),
    path("download-clients/", save_clients_csv_view, name="clients-save"),
    path("download-transactions/", save_transactions_csv_view, name="transactions-save"),
]