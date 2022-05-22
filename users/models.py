from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from creyp.utils import random_string_generator, file_cleanup, image_resize

from PIL import Image
from django_countries.fields import CountryField


STATUS = (
    ("pending", "pending"),
    ("credit", "credit"),
    ("processing", "processing"),
    ("confirming", "confirming"),
    ("error", "error"),
    ("failed", "failed")
)
GENDER = (
    ("female", "female"),
    ("male", "male"),
    ("other", "other")
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="profile-image/%h/%Y/",
                              default="profile-image-placeholder.png")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = CountryField(blank=True)
    signup_confirmation = models.BooleanField(default=False)
    deposit_before = models.BooleanField(default=False)
    referred_by = models.ForeignKey("Profile", on_delete=models.CASCADE, blank=True, null=True)
    refer_clicks = models.IntegerField(default=0, blank=True, null=True)
    refers = models.ManyToManyField(User, related_name="refers", blank=True)
    ip_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
            if self.image.storage.exists(self.image.name):
                image_resize(self.image, 512, 512)


class Wallet(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    btc_address = models.TextField(blank=True, null=True)
    bonus = models.CharField(max_length=10, default="0", blank=True)
    balance = models.CharField(max_length=100, default="00.00", blank=True)
    pin = models.CharField(max_length=6, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.btc_address} - bal : {self.balance}"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=15, choices=STATUS)
    msg = models.TextField(blank=True)
    transactionId = models.CharField(max_length=17, blank=True)
    hash_id = models.CharField(max_length=17, blank=True, null=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-timestamp', '-id']

    def __str__(self):
        return f"user has {self.wallet.balance} | TID: {self.transactionId}"

    def save(self, *args, **kwargs):
        self.hash_id = random_string_generator(size=17)
        super().save(*args, **kwargs)


class AdminWallet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    btc_address = models.TextField(unique=True)
    returns = models.CharField(max_length=100, blank=True)
    bad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.btc_address}"

class AdminTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100, blank=True)
    amount = models.CharField(max_length=100, blank=True)
    btc_address = models.TextField()
    msg = models.TextField(blank=True)
    transactionId = models.CharField(max_length=17, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.plan == "withdraw":
            return f"{self.wallet.btc_address} debited ${self.amount}"
        else:
            return f"{self.wallet.btc_address} transfered ${self.amount}"

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=Profile)
def update_wallet_signal(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


post_delete.connect(
    file_cleanup, sender=Image, dispatch_uid="profile.image.file_cleanup"
)
