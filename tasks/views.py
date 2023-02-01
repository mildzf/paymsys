from django.shortcuts import redirect, render
from django.contrib import messages
from accts.models import Account 


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