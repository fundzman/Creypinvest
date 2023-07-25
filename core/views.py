from django.shortcuts import redirect, render

from creyp.utils import send_contact_us_email, set_cookie_function

from users.models import Profile
from users.decorators import update_user_ip


# Error Code Page Views
@update_user_ip
def error_404_view(request, exception):
    return render(request, "pages/errors/404.html")

@update_user_ip
def dashboard_denial_view(request):
    return render(request, "pages/errors/dashboard_denial.html")

@update_user_ip
def index(request):
    return render(request, "pages/index.html")

@update_user_ip
def referral_view(request, username):
    cookie = request.COOKIES.get("_refered_by", None) == None
    user = request.user
    is_user = str(request.user.username) == str(username)
    context = {}
    if not user.is_authenticated:
        if cookie == True:
            context = {
                "username": username,
                "title": "Congratulation",
                "message": f"You were been referred by {username}, now signup and deposit above $1,000 to get $100 has welcoming gift!",
                "btn": "signup"
            }
            res = render(request, "pages/referral.html", context)
            set_cookie_function("_refered_by", str(username),
                                max_age=500*1900, response=res)
            qs = Profile.objects.filter(user__username=username).first()
            qs.refer_clicks = qs.refer_clicks + 1
            qs.save()
        else:
            try:
                context = {
                    "username": username,
                    "title": "Hey!",
                    "message": f"You have already been referred by {request.COOKIES['_refered_by']}, just create an account and deposit above $1,000 then get your $100 welcoming gift!",
                    "btn": "signup"
                }
            except:
                context = {
                    "username": username,
                    "title": "Hey!",
                    "message": f"You have already been referred, just create an account and deposit above $1,000 then get your $100 welcoming gift!",
                    "btn": "signup"
                }
            res = render(request, "pages/referral.html", context)
    elif user.is_authenticated:
        if is_user:
            context = {
                "username": username,
                "title": f"Sorry {user.username}",
                "message": "You can not refer yourself",
                "btn": "back"
            }
            res = render(request, "pages/referral.html", context)
        else:
            return redirect("dashboard-home")
    return res

@update_user_ip
def about(request):
    return render(request, "pages/about.html", {"type": "About CreypInvest Inc.", "crumbs": ["About Us"]})

@update_user_ip
def contact(request):
    return render(request, "pages/contact.html", {"type": "Contact Support Team At CreypInvest Inc.", "crumbs": ["Contact Us"]})

@update_user_ip
def send_contact_email(request):
    res = render(request, "pages/message_page.html",
                 {"title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        body = request.POST.get("message")
        try:
            send_contact_us_email(request, name, phone,
                                  email, subject, body, toAdmin=True)
            send_contact_us_email(request, name, phone, email, "Email Has Been Recieved",
                                  "Your Email Has Been Received, We Will Get Back To You A Soon As Possible")
            res = render(request, "pages/message_page.html",
                         {"title": "Yay!", "msg": "Your mail has been sent to us"})
        except:
            res = render(request, "pages/message_page.html", {
                         "title": "Oops", "msg": "Sorry, something is wrong with the server but you can mail us at <a href='mailto:creypinvest@gmail.com'>creypinvest@gmail.com</a>"})
    return res
