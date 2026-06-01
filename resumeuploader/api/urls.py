from django.urls import path
from api import views

urlpatterns = [
    path('resume/', views.ProfileView.as_view(), name='resume'),
    path('list/', views.ProfileView.as_view(), name='list'),
    path('list/<int:pk>/', views.ProfileView.as_view(), name='delete'),

    # CandidateList CRUD endpoints
    path('candidate-lists/', views.CandidateListView.as_view(), name='candidate-lists'),
    path('candidate-lists/<int:pk>/', views.CandidateListView.as_view(), name='candidate-list-detail'),

] 