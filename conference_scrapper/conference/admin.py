from django.contrib import admin
from conference_scrapper.conference.models import Conference, ConferenceEdge
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.db.models import Subquery, OuterRef


def link(link, inner_text, target_blank=True):
    target = 'target="_blank"' if target_blank else ''
    return format_html(f'<a href="{link}" {target}>{inner_text}</a>')


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'key_words']
    search_fields = ['title', 'url', 'slug', 'source']
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(ConferenceEdge)
class ConferenceEdgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_conf_1', 'get_conf_2', 'matches']
    search_fields = ['conf_1', 'conf_2', 'matches_len', 'matches', 'source']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        subqs1 = Conference.objects.filter(slug=OuterRef('conf_1')).values('id')
        subqs2 = Conference.objects.filter(slug=OuterRef('conf_2')).values('id')
        qs = qs.annotate(
            conf_1_id=Subquery(subqs1[:1]),
            conf_2_id=Subquery(subqs2[:1])
        )
        return qs

    def get_conf_1(self, obj):
        link_str = link(reverse('admin:conference_conference_change', args=(obj.conf_1_id,)), obj.conf_1)
        return mark_safe(link_str)

    def get_conf_2(self, obj):
        link_str = link(reverse('admin:conference_conference_change', args=(obj.conf_2_id,)), obj.conf_2)
        return mark_safe(link_str)

    get_conf_1.short_description = 'Conference 1'
    get_conf_2.short_description = 'Conference 2'
