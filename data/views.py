from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import openai
from data.models import UserProfile, JobPosting, JobApplication
from .serializers import Item, RegisterApplicant, RegisterHR, JobPostingHR, JobPostsHR, JobApply, ApplicantApplications, JobApplicantDetail, ApplicantDetail, JobPostingDetail
import jwt, datetime
openai.api_key = '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'
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

@api_view(['GET'])
def getData(request):
    items = UserProfile.objects.all()
    serializer = Item(items, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
    serializer = Item(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

class RegisterViewApplicant(APIView):
    def post(self, request):
        serializer = RegisterApplicant(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Status": "Success"})

class RegisterViewHR(APIView):
    def post(self, request):
        serializer = RegisterHR(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginAppliant(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = UserProfile.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not Found")
        
        if not user.password == password:
            raise AuthenticationFailed("Incorrect Password")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'status': "Success"
        }
        return response

class LoginHR(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = UserProfile.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not Found")
        
        if not user.password == password:
            raise AuthenticationFailed("Incorrect Password")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'status': "Success"
        }
        return response

class UserViewApplicant(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = UserProfile.objects.filter(id=payload['id']).first()
        serializer = RegisterApplicant(user)
        return Response(serializer.data)

class UserViewHR(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = UserProfile.objects.filter(id=payload['id']).first()
        serializer = RegisterHR(user)
        print(user.id)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class JobPost(APIView):
    def post(self, request):
        # description_o = request.data["description"]
        # title = request.data["title"]
        # # token='ZgiwzoNzLwOM-UC1XULu0p6yIDrTOrqIcSFSKwCdSR6yef_KUTPgP-SZF1ux5vDrIuNSXg.'
        # prompt = '''Please take the following job description and format it into a consistent and organized format:
        #             Job Title:''' + title + '''Company: [Company]
        #             Location: [Location]
        #             Job Description: [Job Description]
        #             Eligibility Criteria: [Eligibility Criteria]
        #             If any of the mentioned parts are not provided in the given input, please display 'N/A' for that section. Consider the following Job Description''' + description_o 
        # response = get_completion(prompt)
        # print(response)
        serializer = JobPostingHR(data=request.data)
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('Unauthenticated!')
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated!')
        # user = UserProfile.objects.filter(id=payload['id']).first()

        # if user is None:
        #     raise AuthenticationFailed('User not Found')
        ID = request.data["poster"]
        print(ID)
        user = UserProfile.objects.filter(id=ID).first()
        serializer.is_valid(raise_exception=True)
        serializer.save(poster=user)
        return Response(serializer.data)
class PostingsHR(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = UserProfile.objects.filter(id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed('User not Found')
        job_posts = JobPosting.objects.filter(poster=user)
        serializer = JobPostsHR(job_posts, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def AllJobs(APIView):
    items = JobPosting.objects.all()
    serializer = JobPostsHR(items, many = True)
    return Response(serializer.data)

    
class JobApplyApplicant(APIView):
    def post(self, request):
        serializer = JobApply(data=request.data)

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = UserProfile.objects.filter(id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed('User not Found')

        if serializer.is_valid():
            # Set the qualified_round based on the job application's round
            serializer.save(applicant=user, qualified_round=0)
            return Response(serializer.data)
class ApplicantApplicationsView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        applicant_id = payload['id']
        applications = JobApplication.objects.filter(applicant=applicant_id)
        
        serializer = ApplicantApplications(applications, many=True)

        job_ids = applications.values_list('job_posting', flat=True)  # Get list of job IDs
        job_details = JobPosting.objects.filter(id__in=job_ids)  # Fetch job details
        
        data = {
            'applications': serializer.data,
            'job_details': JobPostingDetail(job_details, many=True).data,
        }

        return Response(data)
class JobApplicantsView(APIView):
    def get(self, request, job_id):
        try:
            job = JobPosting.objects.get(id=job_id)
        except JobPosting.DoesNotExist:
            return Response({'error': 'Job not found'})

        applicants = JobApplication.objects.filter(job_posting=job)

        serializer = JobApplicantDetail(applicants, many=True)

        data = {
            'job_details': JobPostingDetail(job).data,
            'applicants': serializer.data,
        }

        return Response(data)
class JobDetailsView(APIView):
    def get(self, request, job_id):
        try:
            job = JobPosting.objects.get(id=job_id)
        except JobPosting.DoesNotExist:
            return Response({'error': 'Job not found'})

        data = {
            'job_details': JobPostingDetail(job).data,
        }

        return Response(data)