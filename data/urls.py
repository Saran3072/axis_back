from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/', views.addItem),
    path('register-applicant/', views.RegisterViewApplicant.as_view()),
    path('register-hr/', views.RegisterViewHR.as_view()),
    path('login-applicant/', views.LoginAppliant.as_view()),
    path('login-hr/', views.LoginHR.as_view()),
    path('user-applicant/', views.UserViewApplicant.as_view()),
    path('job-posting/', views.JobPost.as_view()),
    path('user-hr/', views.UserViewHR.as_view()),
    path('postings-hr/', views.PostingsHR.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('all-jobs-applicant/', views.AllJobs),
    path('apply-applicant/', views.JobApplyApplicant.as_view()),
    path('applied-jobs/', views.ApplicantApplicationsView.as_view()),
    path('job-applicants/<int:job_id>/', views.JobApplicantsView.as_view()),
    path('job-details/<int:job_id>/', views.JobDetailsView.as_view()),
]
