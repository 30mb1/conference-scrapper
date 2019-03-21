from django.contrib import admin
from conference_scrapper.conference.models import Conference, ConferenceEdge
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Conference)
class Conference(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(ConferenceEdge)
class Conference(admin.ModelAdmin):
    pass