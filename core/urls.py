from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('pdf/',GeneratePdf.as_view()),
    path('excel/',ExportImportExcel.as_view()),
    path('register/',RegisterUser.as_view()),
    path('student/',StudentAPI.as_view()),
    path('generic-student/',StudentGeneric.as_view()),
    path('generic-student-update/<id>/',StudentGenericUpdate.as_view()),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= staticfiles_urlpatterns()