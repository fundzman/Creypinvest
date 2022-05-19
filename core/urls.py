from django.urls import path
from core.views import about, contact, send_contact_email

urlpatterns = [
    path("about-us/", about, name="about-us"),
    path("contact-us/", contact, name="contact-us"),
    path("send-mail/contact-us/", send_contact_email, name="send_contact_email"),
]
