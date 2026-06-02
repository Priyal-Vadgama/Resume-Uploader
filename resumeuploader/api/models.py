from django.db import models

# Create your models here.
class Profile(models.Model):
    """Represents a candidate profile with personal details and uploaded files.

    Stores the candidate's name, email, date of birth, state, gender,
    location, and optional profile image and resume file uploads.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(max_length=50)
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pimage = models.ImageField(upload_to='pimages', blank=True)
    resume = models.FileField(upload_to='resume', blank=True)

class Skill(models.Model):
    """Represents a professional skill or qualification for a candidate.

    Associates a skill name (e.g., "Python", "Project Management") with
    a proficiency level (beginner, intermediate, advanced, expert) and
    years of experience. Each skill belongs to a single Profile.
    """
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    EXPERT = 'expert'
    PROFICIENCY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='skills',
    )
    name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default=INTERMEDIATE,
    )
    years_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-proficiency', 'name']
        unique_together = ['profile', 'name']

    def __str__(self):
        return f"{self.name} ({self.proficiency})"


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
