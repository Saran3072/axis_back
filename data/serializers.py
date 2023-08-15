from rest_framework import serializers
from data.models import UserProfile, JobPosting, JobApplication

class Item(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class RegisterApplicant(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'mobile', 'password', 'degree', 'major', 'cgpa', 'passout', 'job_role', 'exp_desc', 'company', 'college', 'years', 'skills']
        extra_kwargs = {
            "password": {"write_only": True}
        }
class RegisterHR(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'mobile', 'password', 'company']
        extra_kwargs = {
            "password": {"write_only": True}
        }
class JobPostingHR(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'description_enhance', 'poster', 'company_name', 'expected_cgpa', 'package', 'number_of_openings', 'expected_interviewees']
class JobPostsHR(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'description', 'title', 'poster', 'company_name', 'package']
class JobApply(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['applicant', 'job_posting', 'cover_letter', 'resume', 'qualified_round']
class ApplicantApplications(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job_posting', 'cover_letter', 'resume', 'qualified_round', 'applied_at']
class JobPostingDetail(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'company_name', 'package', 'number_of_openings', 'expected_interviewees']
class ApplicantDetail(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'email']
class JobApplicantDetail(serializers.ModelSerializer):
    applicant = ApplicantDetail()
    job_posting = JobPostingDetail()
    class Meta:
        model = JobApplication
        fields = ['applicant', 'job_posting', 'cover_letter', 'resume', 'applied_at', 'qualified_round']
