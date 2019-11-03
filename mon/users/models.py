from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from projects.models import Loc
import enum


class UserTypes(enum.Enum):
    USER = "USER"
    TRADER = "TRADER"


class UserStatus(enum.Enum):
    COMPLETE = 1
    INCOMPLETE = 0

class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    accepted_terms_condition = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def is_trademan(self):
        return self.groups.filter(name='trademan').exists()



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, models.DO_NOTHING, blank=True, null=True)
    username = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_city = models.ForeignKey(Loc, models.DO_NOTHING, blank=True, null=True)
    phonenumber = models.CharField(max_length=255)
    subscription_sms_alerts = models.IntegerField(blank=True, null=True)
    subscription_newsletter = models.IntegerField(blank=True, null=True)
    subscription_surveys = models.IntegerField(blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'user_profiles'