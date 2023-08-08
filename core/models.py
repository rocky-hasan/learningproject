from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.
class ContactModelForm(models.Model):
    username = models.CharField(max_length=70, null=True)
    email = models.EmailField(max_length=100)
    Phone_number = models.CharField(max_length=200, null=True)
    desc = models.TextField()

    def __str__(self):
        return self.username


class Allcourse(models.Model):
    courseName = models.CharField(max_length=150, primary_key=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    coursefee = models.IntegerField()
    courseduration = models.IntegerField()
    syllabus = RichTextField(default='syllabus')
    aboutsyllabus = RichTextField(default='aboutsyllabus')
    stars = models.IntegerField(default=3)

    def __str__(self):
        return self.courseName


class Trainer(models.Model):
    trainer_name = models.CharField(max_length=50)
    trainer_designation = models.CharField(max_length=100)
    trainer_experience = models.DecimalField(max_digits=5, decimal_places=2)
    course = models.ForeignKey(Allcourse, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.trainer_name


class Register(models.Model):
    candidateId = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    fathers_name = models.CharField(max_length=20, null=False)
    Phone_number = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField(max_length=150)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, default='Basic')
    computer_knowledge = models.CharField(max_length=100, null=False)
    course = models.CharField(max_length=80)
    timestamp = models.DateField(auto_now_add=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.email


class Payments(models.Model):
    name = models.ForeignKey(Register, on_delete=models.CASCADE)
    amountPaid = models.IntegerField()
    balance = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default='unpaid')

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)


class Attendance(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70)
    date = models.CharField(max_length=50)
    logintime = models.CharField(max_length=50)
    logouttime = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email
