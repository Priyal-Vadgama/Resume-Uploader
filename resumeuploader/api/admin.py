"""Django admin configuration for the Resume Uploader API.

Registers Profile, CandidateList, and Skill models with the Django
admin interface, including custom list displays and filterable widgets.
"""

from django.contrib import admin
from api.models import Profile, CandidateList, Skill
# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    """Admin interface for the Profile model.

    Displays all candidate fields as list columns for easy browsing
    and inline editing in the Django admin.
    """

    list_display = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']
    search_fields = ['name', 'email']

@admin.register(CandidateList)
class CandidateListAdmin(admin.ModelAdmin):
    """Admin interface for the CandidateList model.

    Provides a filterable horizontal widget for selecting candidates
    and search fields for title and description lookups.
    """
    list_display = ['id', 'title', 'created_at', 'updated_at']
    filter_horizontal = ['candidates']
    search_fields = ['title', 'description']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin interface for the Skill model.

    Provides list filtering by proficiency level, search by skill
    name, and autocomplete for the profile foreign key.
    """
    list_display = ['id', 'name', 'proficiency', 'years_experience', 'profile']
    list_filter = ['proficiency']
    search_fields = ['name', 'profile__name', 'profile__email']
    autocomplete_fields = ['profile']
