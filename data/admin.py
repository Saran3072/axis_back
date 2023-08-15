from django.contrib import admin
from .models import JobApplication, noofrounds, JobPosting, UserProfile
admin.site.register(JobApplication)
admin.site.register(noofrounds)
admin.site.register(JobPosting)
# admin.site.register(JobCategory)
admin.site.register(UserProfile)
# admin.site.register(ApplicationStatus)

# Register your models here.
