from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics


class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentGenericUpdate(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field ='id'
from .helpers import *
import datetime
class GeneratePdf(APIView):
    def get(self, request):
        student_objs = Student.objects.all()
        params={
            'today':datetime.date.today(),
            'student_objs':student_objs
        }
        file_name ,status=save_pdf(params)
        if not status:
            return Response ({'status':400})

        return Response ({'status':200,'path':f"/media/{file_name}.pdf"})
import pandas as pd
class ExportImportExcel(APIView):
    def get(self,request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs,many=True)
        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv(str(settings.BASE_DIR)+f"/static/excel{uuid.uuid4()}.csv",encoding="UTF-8")

        return Response({'status':200})

    def post (self,request):
        excel_upload_obj = ExcelFileUpload.objects.create(excel_file_upload =request.FILES['files'])
        df = pd.read_csv(f"{settings.BASE_DIR}/static/{excel_upload_obj.excel_file_upload}")
        print(df.values.tolist())

        return Response ({'status':200})












# Create your views here.
class RegisterUser(APIView):

    def post(self, request):
        serializer =UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status':403,'error':serializer.errors,'message':'Kuchh to galat hua hain'})
        serializer.save()
        user=User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({'status':200,'refresh':str(refresh),'access':str(refresh.access_token),'payload':serializer.data,'message':'user saved successfully'})
from .models import Student
class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_obj = Student.objects.all()
        serializer = StudentSerializer(student_obj,many=True)
        return Response({'status':200,'payload':serializer.data})