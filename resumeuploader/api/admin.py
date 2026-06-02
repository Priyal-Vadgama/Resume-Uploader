from django.contrib import admin
from api.models import Profile, CandidateList
# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']

@admin.register(CandidateList)
class CandidateListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    filter_horizontal = ['candidates']
    search_fields = ['title', 'description']
