from django.db import models
from django.utils import timezone

class Cms(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    url_key = models.CharField(max_length=255, db_column='url-key', db_index=True)  # Field renamed to remove unsuitable characters.
    meta_title = models.CharField(db_column='meta-title', max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    meta_description = models.TextField(db_column='meta-description', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    meta_keywords = models.TextField(db_column='meta-keywords', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    status = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    #
    # class Meta:
    #     db_table = 'cms'