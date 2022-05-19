import os
from django.conf import settings
import string
import random
import datetime
from django.core.mail import send_mail
import threading
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.db.models import FileField

from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.http import HttpResponse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
currentDT = datetime.datetime.now()
ADMIN_EMAIL = settings.EMAIL_HOST_USER


def set_cookie_function(key, value, max_age=None, response=None):
    if response == None:
        response = HttpResponse("sorry, you are not allowed here, please go back <a href='javascript:history.back()'>BACK!</a>")
    response.set_cookie(str(key), value, max_age=max_age)
    return response


def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
            if field and isinstance(field, FileField):
                inst = kwargs["instance"]
                f = getattr(inst, fieldname)
                m = inst.__class__._default_manager
                if (
                    hasattr(f, "path")
                    and os.path.exists(f.path)
                    and not m.filter(
                        **{"%s__exact" % fieldname: getattr(inst, fieldname)}
                    ).exclude(pk=inst._get_pk_val())
                ):
                    try:
                        default_storage.delete(f.path)
                    except:
                        pass


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)


def truncate_string(value, max_length=45, suffix="skt"):
    string_value = str(value)
    string_truncated = string_value[:min(
        len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return suffix+string_truncated


def random_string_generator(size=50, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# ROT13 ENCRYPTION
rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                           'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')


# Function to translate plain text
def rot13_encrypt(text):
    return text.translate(rot13trans)
# Account Section


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

milliseconds = str(currentDT.microsecond).strip()
def send_contact_us_email(request, name=None, phone=None, user_email=None, subject=None, body=None, toAdmin=False):
    email_subject = subject
    email_body = render_to_string('account/email/contact_us_email_sent.html', {
        'email_subject': email_subject,
        'email': user_email,
        'name': name,
        'phone': phone,
        'body': body,
        'toAdmin': toAdmin
    }, request)
    text_content = strip_tags(email_subject)
    user_email = user_email.replace("@", f"+{milliseconds}@")
    if toAdmin == True:
        email = send_mail(
            email_subject, text_content, ADMIN_EMAIL, [ADMIN_EMAIL], html_message=email_body)
    else:
        email = send_mail(
            email_subject, text_content, ADMIN_EMAIL, [user_email], html_message=email_body)

    if not settings.DEBUG:
        EmailThread(email).start()

def send_alert_mail(request, email_subject, user_email, email_message, email_image="alert.png", html_message=None, email_ip=None, email_user=None):
    email_subject = email_subject
    try:
        if not email_user == None:
            user_email = email_user.email
    except:
        user_email = user_email
    email_body = render_to_string('account/email/alert_email.html', {
        'email_subject': email_subject,
        'user_email': user_email,
        'email_message': email_message,
        'html_message': html_message,
        'email_image': email_image,
        'email_ip': email_ip
    }, request)
    text_content = strip_tags(html_message)
    if email_message:
        text_content = strip_tags(email_message)
    user_email = user_email.replace("@", f"+{milliseconds}@")
    email = send_mail(
        email_subject, text_content, ADMIN_EMAIL, [user_email], html_message=email_body)

    if not settings.DEBUG:
        EmailThread(email).start()