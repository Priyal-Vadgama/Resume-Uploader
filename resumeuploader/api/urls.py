"""URL configuration for the API application.

Defines endpoints for candidate profile uploads, listing, retrieval,
deletion, CandidateList CRUD operations, and Skill management.
"""

from django.urls import path
from api import views

urlpatterns = [
    path('resume/', views.ProfileView.as_view(), name='resume'),
    path('list/', views.ProfileView.as_view(), name='list'),
    path('list/<int:pk>/', views.ProfileView.as_view(), name='delete'),

    # CandidateList CRUD endpoints
    path('candidate-lists/', views.CandidateListView.as_view(), name='candidate-lists'),
    path('candidate-lists/<int:pk>/', views.CandidateListView.as_view(), name='candidate-list-detail'),

    # Skill CRUD endpoints
    path('skills/', views.SkillView.as_view(), name='skills'),
    path('skills/<int:pk>/', views.SkillView.as_view(), name='skill-detail'),

]