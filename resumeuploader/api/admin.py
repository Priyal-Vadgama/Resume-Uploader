"""Django admin configuration for the Resume Uploader API.

Registers Profile and CandidateList models with the Django admin
interface, including custom list displays and filterable many-to-many
widgets.
"""

from django.contrib import admin
from api.models import Profile, CandidateList
# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    """Admin interface for the Profile model.

    Displays all candidate fields as list columns for easy browsing
    and inline editing in the Django admin.
    """

    list_display = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']

@admin.register(CandidateList)
class CandidateListAdmin(admin.ModelAdmin):
    """Admin interface for the CandidateList model.

    Provides a filterable horizontal widget for selecting candidates
    and search fields for title and description lookups.
    """
    list_display = ['id', 'title', 'created_at', 'updated_at']
    filter_horizontal = ['candidates']
    search_fields = ['title', 'description']
