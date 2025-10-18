from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/%y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')  
    title = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='lessons/videos/%y/%m/%d', blank=True, null=True)
    attachment = models.FileField(upload_to='lessons/files/%y/%m/%d', blank=True, null=True)  # PDF أو ملفات أخرى
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username

class Messages(models.Model):
    name = models.TextField(max_length=100)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"