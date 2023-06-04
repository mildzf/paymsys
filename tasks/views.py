import subprocess
from django.shortcuts import redirect, render
from django.contrib import messages
import os
from django.http import  FileResponse
from accts.models import Account

import datetime
from django.core.management import call_command

def save_database_view(request):
    directory = 'database_backups'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get the current date and time as a string
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d-%H-%M-%S")

    # Save the fixture file using the current date in the file name
    fixture_filename = f"db_fixture_{date_str}.json"
    fixture_path = os.path.join(directory, fixture_filename)
    try:
        with open(fixture_path, 'w') as f:
            call_command('dumpdata', stdout=f)
            messages.success(request, "Database saved successfully!!!")
    except Exception as e:
        messages.error(request, 'Error saving database!!!')

    return redirect(request.META.get('HTTP_REFERER'))





def save_clients_csv_view(request):
    # Run the save_clients command using subprocess
    subprocess.run(['python', 'manage.py', 'save_clients_as_csv'], stdout=subprocess.PIPE)

    # Offer the user the option to download the CSV file
    csv_path = os.path.join(os.getcwd(), 'database_backups/clients.csv')
    with open(csv_path, 'rb') as csv_file:
        response = FileResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="clients.csv"'
        return response

def save_accts_csv_view(request):
    # Run the save_clients command using subprocess
    subprocess.run(['python', 'manage.py', 'save_accts_as_csv'], stdout=subprocess.PIPE)

    # Offer the user the option to download the CSV file
    csv_path = os.path.join(os.getcwd(), 'database_backups/accts.csv')
    with open(csv_path, 'rb') as csv_file:
        response = FileResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="accts.csv"'
        return response

def save_transactions_csv_view(request):
    # Run the save_clients command using subprocess
    subprocess.run(['python', 'manage.py', 'save_transactions_as_csv'], stdout=subprocess.PIPE)

    # Offer the user the option to download the CSV file
    csv_path = os.path.join(os.getcwd(), 'database_backups/transactions.csv')
    with open(csv_path, 'rb') as csv_file:
        response = FileResponse(csv_file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        return response


def charge_accounts(request):
    if request.method=="POST":
        active_accounts = Account.objects.active()
        try:
            for account in active_accounts:
                new_balance = account.balance + account.service_fee
                account.balance = new_balance
                account.save()
            messages.success(request, "All active account balances have been updated!")
        except Exception as e:
            messages.error(request,
                f"Something went wrong!!! See details below: \n {e} \n Notify admin with error message above. ")
    else:
        return render(request, "tasks/charge_accts.html")
    return redirect("dashboard")