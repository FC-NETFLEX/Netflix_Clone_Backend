from django.contrib.auth.models import AbstractUser
from django.db import models
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Payment(models.Model):
    cc_number = CardNumberField('card number')  # 카드번호
    cc_expiry = CardExpiryField('expiration date')  # 유효기간
    cc_code = SecurityCodeField('CVV/CVC')


class User(AbstractUser):
    email = models.EmailField('이메일', unique=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)


class Profile(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True)


