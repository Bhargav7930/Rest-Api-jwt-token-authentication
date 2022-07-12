from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    age=models.IntegerField(default=18)
    father_name = models.CharField(max_length=100)
    address =models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to = 'excel')
    