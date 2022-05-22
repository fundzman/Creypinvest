from django.core.files.storage import default_storage
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from users.models import Profile
from creyp.utils import set_cookie_function, send_alert_mail


def get_client_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def update_user_ip(function):
    def wrap(request, *args, **kwargs):
        res = function(request, *args, **kwargs)
        user_ip = get_client_ip(request)
        js_user_ip = request.COOKIES.get("_user_ip", None) == None
        sent_mail_before = request.COOKIES.get(
            "alert_message_sent", False) == False
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            try:
                path = f"{request.user.profile.image.path}"
                is_image = default_storage.exists(path)
                print(is_image)
                if is_image == False:
                    profile.image = "profile-image-placeholder.png"
                    profile.save()
            except:
                pass
            if profile.user.username == request.user.username:
                if not js_user_ip == True:
                    js_user_ip = request.COOKIES['_user_ip']
                    if profile.ip_address:
                        qs_ip_address = profile.ip_address
                        if not qs_ip_address == js_user_ip:
                            try:
                                if sent_mail_before == True:
                                    rest_url = request.build_absolute_uri(
                                        '/auth/account/password/change/?next=/dashboard/')
                                    html_msg = f'<a style="border: 1px solid #673ab7;padding: 5px 10px;border-radius: 24px;color: #fff;background: #673ab7;" href="{rest_url}" class="btn btn-primary border">Change Password</a>'
                                    send_alert_mail(request=request, email_subject="Alert - New Device Login", user_email=request.user.email,
                                                    email_message="A new device (or new IP Address) just accessed your account. You can change your password if its not you", html_message=html_msg)
                                    set_cookie_function(
                                        "alert_message_sent", True, max_age=3600, response=res)
                            except:
                                set_cookie_function(
                                    "alert_message_sent", True, max_age=3600, response=res)
                        elif not user_ip == js_user_ip:
                            profile.ip_address = js_user_ip
                            profile.save()
                        else:
                            if not qs_ip_address == user_ip:
                                profile.ip_address = user_ip
                                profile.save()
                    else:
                        profile.ip_address = js_user_ip
                        profile.save()
                return res
            else:
                raise PermissionDenied
        else:
            return res
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def deposit_before(function):
    def wrap(request, *args, **kwargs):
        res = function(request, *args, **kwargs)
        if request.user.is_authenticated:
            if request.user.profile.deposit_before == True:
                return res
            else:
                return redirect("dashboard-denial")
        else:
            return redirect("account_login")
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
