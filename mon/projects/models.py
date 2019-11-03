from django.db import models
from django.conf import settings
import uuid

from django.utils import timezone
import enum


class ProjectStatus(enum.Enum):
    INACTIVE = "0"
    PROFILE_ACTIVE = "1"
    APPROVED = "2"


class County(models.Model):
    county_name = models.CharField(max_length=255)
    county_code = models.CharField(max_length=2,blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    url_key = models.CharField(max_length=255, blank=True, null=True)
    seo_sort = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'counties'


class Loc(models.Model):
    county = models.ForeignKey(County, models.DO_NOTHING, blank=True, null=True)
    loc_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    url_key = models.CharField(max_length=255, blank=True, null=True)
    seo_sort = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        # managed = True
        # db_table = 'locs'
        unique_together = (('county', 'loc_name'),)


class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField()
    loc = models.ForeignKey(Loc, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="user_project", blank=True, null=True)
    tradesman = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="winner_trader_project", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'projects'


class ActiveProjectManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProjectManager, self).get_queryset().filter(status=ProjectStatus.APPROVED.value)


class ProjectsToTradesman(models.Model):
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    tradesman = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    # class Meta:
    #     managed = True
    #     db_table = 'projects_to_tradesman'



