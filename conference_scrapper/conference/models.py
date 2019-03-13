from django.db import models
from django.contrib.postgres import fields


class Conference(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    key_dates = fields.JSONField(default=dict)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    key_words = fields.ArrayField(models.CharField(max_length=64), null=True, blank=True)