from polls.models import Poll
from polls.models import Choice
from django.contrib import admin


class ChoiceInline(admin.TabularInline):
    """docstring for ChoiceInline"""
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    """docstring for PollAdmin"""
    fieldsets = [
        (None,              {"fields": ["question"]}),
        ("Date infomation", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_display = ('question', 'pub_date', 'was_published_recently')
    inlines = [ChoiceInline]
    list_filter = ["pub_date"]
    search_fields = ["question"]
    date_hierarchy = "pub_date"

admin.site.register(Poll, PollAdmin)
