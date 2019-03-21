from django.db import models
from django.contrib.postgres import fields


class Conference(models.Model):
    source = models.CharField(max_length=32)
    title = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    slug = models.CharField(max_length=32, db_index=True)
    year = models.IntegerField(null=True, blank=True)
    key_dates = fields.JSONField(default=dict, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    key_words = fields.ArrayField(models.CharField(max_length=256), null=True, blank=True)