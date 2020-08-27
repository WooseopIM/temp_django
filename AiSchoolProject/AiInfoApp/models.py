from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AiClass(models.Model):
    class_num = models.IntegerField()
    teacher = models.CharField(max_length=10)
    class_room = models.CharField(max_length=10)


class AiStudent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student")
    # AiClass의 반이 AiStudent의 학생을 지칭할 때 이름(related_name)을 student로 지정
    participate_class = models.ForeignKey(
        AiClass, on_delete=models.CASCADE, related_name="student")
    name = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=15)


# 1:N
class StudentPost(models.Model):
    # AiStudent의 학생이 StudentPost의 글을 지칭할 때 이름(related_name)을 post로 지정
    writer = models.ForeignKey(
        AiStudent, on_delete=models.SET_NULL, null=True, related_name="post")
    intro = models.TextField()
