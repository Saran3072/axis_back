from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    cgpa = models.DecimalField(blank=True, max_digits=2, decimal_places=1, null=True)
    current = models.BooleanField(blank=True, default=True)
    years = models.IntegerField(default=0, blank=True)
    company = models.CharField(max_length=255, blank=True)
    college = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    TYPES = (
        ('applicant', 'Applicant'),
        ('hr', 'HR'),
    )
    user_type = models.CharField(choices=TYPES, max_length=50)
    job_role = models.CharField(null=True, max_length=50, blank=True)
    exp_desc = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    degree = models.CharField(null=True, max_length=100, blank=True)
    major = models.CharField(null=True, max_length=100, blank=True)
    passout = models.IntegerField(null=True, blank=True)
    # Add more fields as needed: contact info, skills, experience, etc.

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    description_enhance = models.TextField(default= None, null=True)
    poster = models.ForeignKey(UserProfile, default = None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    company_name = models.CharField(max_length=200)
    expected_cgpa = models.DecimalField(max_digits=2, decimal_places=1)
    package = models.CharField(max_length=100)
    number_of_openings = models.PositiveIntegerField()
    expected_interviewees = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class noofrounds(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    no_of_rounds = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.job_posting.title} - {self.no_of_rounds} Rounds"

class JobApplication(models.Model):
    applicant = models.ForeignKey(UserProfile, default = None, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, default = None, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    qualified_round = models.PositiveIntegerField(default=0)
