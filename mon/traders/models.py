from django.db import models
from django.conf import settings
from datetime import datetime
import enum

class TraderType(models.Model):
    parent_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(unique=True, max_length=255)
    name_plural = models.CharField(max_length=255)
    url_key = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    suggested_title = models.CharField(max_length=255, blank=True, null=True)
    suggested_description = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    #
    # class Meta:
    #     managed = True
    #     db_table = 'trader_types'


class TradesmanStatus(enum.Enum):
    COMPLETE = 1
    INCOMPLETE = 0
    APPROVED = 2


class ActiveTradesmanManager(models.Manager):
    def get_queryset(self):
        return super(ActiveTradesmanManager, self).get_queryset().filter(status=TradesmanStatus.APPROVED.value)


class Tradesman(models.Model):
    username = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    address_city = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    subscription_sms_alerts = models.IntegerField()
    subscription_newsletter = models.IntegerField()
    subscription_surveys = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    objects = models.Manager()  # The default manager.
    approved_objects = ActiveTradesmanManager()

    #
    # class Meta:
    #     managed = True
    #     db_table = 'tradesmen'



class TradesmanFeedback(models.Model):
    project_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    tradesman_id = models.PositiveIntegerField()
    type = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        # managed = True
        # db_table = 'tradesman_feedbacks'
        unique_together = (('project_id', 'user_id', 'tradesman_id'),)


class TradesmanProfile(models.Model):
    photo = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    profile = models.TextField()
    company = models.CharField(max_length=255, blank=True, null=True)
    username_slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    no_feedbacks = models.IntegerField(blank=True, null=True)
    percent_positives = models.IntegerField(blank=True, null=True)
    photo_id_card = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'tradesman_profiles'


class TradesmanToTypes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey(TraderType, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tradesman_to_types'
        unique_together = (('user', 'type'),)