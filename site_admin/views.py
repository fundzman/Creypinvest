from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from users.models import AdminTransaction as AT, Wallet, Transaction, Profile
from creyp.utils import send_alert_mail


def index_view(request):
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:  
        return render(request, "site/admin/index.html")
    else:
        raise PermissionDenied


def transaction_deposit_view(request):
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        qs = AT.objects.all()
        qsd = []
        for qsr in qs:
            if not qsr.plan == 'withdraw':
                qsd.append(qsr)
        return render(request, "site/admin/admin-deposit.html", {"objects": qsd})
    else:
        raise PermissionDenied


def transaction_del_view(request, id):
    qs = AT.objects.filter(id=id).first()
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    user = request.user
    if not qs is None and not tasc is None and user.is_authenticated and user.is_staff == True and user.is_active == True:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" href="{url}" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Rejected",
                            user_email=user_email, email_message=f"Your Deposit Request For ${amount} Has Been Declined", email_image="transaction-declined.png", html_message=html_msg)
        except:
            pass
        tasc.status = "failed"
        tasc.msg = f"Your ${qs.amount} Deposit Request Was Rejected"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qs.delete()
        return redirect("admin-transaction-deposit")
    else:
        raise PermissionDenied


def transaction_accept_view(request, id):
    user = request.user
    qs = AT.objects.filter(id=id).first()
    qsr = Wallet.objects.filter(user=qs.wallet.user).first()
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    profile = Profile.objects.filter(user=qs.wallet.user.user).first()
    if not qs is None and not qsr is None and not tasc is None and user.is_authenticated and user.is_staff == True and user.is_active == True:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/')
            html_msg = f'<a href="{url}" style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject="Deposit Request Accepted",
                            user_email=user_email, email_message=f"Your Account Has Been Credited ${amount}",
                            email_image="transaction-accept.png", html_message=html_msg)
        except:
            pass
        tasc.status = "credit"
        tasc.msg = f"Your Account has been credited ${qs.amount}"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qsr.balance = float(qsr.balance) + float(qs.amount)
        qsr.save()
        profile.deposit_before = True
        profile.save()
        qs.delete()
        return redirect("admin-transaction-deposit")
    else:
        raise PermissionDenied


def transaction_withdraw_view(request):
    user = request.user
    if user.is_authenticated and user.is_staff == True and user.is_active == True:
        qs = AT.objects.all()
        qsd = []
        for qsr in qs:
            if qsr.plan == 'withdraw':
                qsd.append(qsr)
        return render(request, "site/admin/admin-withdraw.html", {"objects": qsd})
    else:
        raise PermissionDenied

def withdraw_accept_view(request, id):
    qs = AT.objects.filter(id=id).first()
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    user = request.user
    if not qs is None and not tasc is None and user.is_authenticated and user.is_staff == True and user.is_active == True:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/payments/')
            html_msg = f'<a style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" href="{url}" class="rounded-pill border">Dashboard</a>'
            send_alert_mail(request, email_subject=f"About Your Withdrawal Payment Of ${amount}",
                            user_email=user_email, email_message=f"We Have Confirmed Your Debit Transfer", email_image="transaction-accept.png", html_message=html_msg)
        except:
            pass
        tasc.status = "failed"
        tasc.msg = f"-${qs.amount} Debit"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qs.delete()
        return redirect("admin-transaction-withdraw")
    else:
        raise PermissionDenied

def withdraw_decline_view(request, id):
    user = request.user
    qs = AT.objects.filter(id=id).first()
    qsr = Wallet.objects.filter(user=qs.wallet.user).first()
    tasc = Transaction.objects.filter(transactionId=qs.transactionId).first()
    profile = Profile.objects.filter(user=qs.wallet.user.user).first()
    if not qs is None and not qsr is None and not tasc is None and user.is_authenticated and user.is_staff == True and user.is_active == True:
        try:
            user_email = qs.wallet.user.user.email
            amount = qs.amount
            url = request.build_absolute_uri('/dashboard/payments/')
            html_msg = f'<a href="{url}" style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" class="rounded-pill border">Payments</a>'
            send_alert_mail(request, email_subject="Money Reversed",
                            user_email=user_email, email_message=f"Your Previous Debit Of ${amount} Has Been Reversed Back To Your Account",
                            email_image="transaction-accept.png", html_message=html_msg)
        except:
            pass
        tasc.status = "error"
        tasc.msg = f"+${qs.amount} Was Reversed"
        tasc.transactionId = qs.transactionId
        tasc.save()
        qsr.balance = float(qsr.balance) + float(qs.amount)
        qsr.save()
        profile.deposit_before = True
        profile.save()
        qs.delete()
        return redirect("admin-transaction-withdraw")
    else:
        raise PermissionDenied