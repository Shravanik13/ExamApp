from django.db import models

# Create your models here.
class Question(models.Model):
    qno=models.IntegerField(primary_key=True)
    qtext=models.CharField(max_length=100)
    answer=models.CharField(max_length=100)
    op1=models.CharField(max_length=50)
    op2=models.CharField(max_length=50)
    op3=models.CharField(max_length=50)
    op4=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)

    class Meta:
        db_table="question"

class UserData(models.Model):
    username=models.CharField(max_length=20, primary_key=True)
    password=models.CharField(max_length=20)
    phno=models.IntegerField()

    class Meta:
        db_table='userdata' #mapping the model with the table in the database

class Result(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    subject=models.CharField(max_length=20)
    marks=models.IntegerField()

    class Meta:
        db_table='result'