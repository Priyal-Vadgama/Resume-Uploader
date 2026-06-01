from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(max_length=50)
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pimage = models.ImageField(upload_to='pimages', blank=True)
    resume = models.FileField(upload_to='resume', blank=True)

class CandidateList(models.Model):
    """Represents a curated list of candidates for review or shortlisting.

    Tracks metadata about when the list was created and last updated,
    along with an optional description of the list's purpose (e.g.,
    "Q3 Frontend Candidates", "Backend Shortlist").
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    candidates = models.ManyToManyField(Profile, related_name='candidate_lists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title