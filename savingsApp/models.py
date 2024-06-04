from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator

from datetime import datetime
import uuid


# Create your models here.
class Member(models.Model):
    contact_regex = r'^(\+256|0)\d{9}$'   # Regex for contact
    contact_validator = RegexValidator(
    regex=contact_regex,
    message='Enter a valid Country contact'
    )

    name_regex = r'^(?=.{1,100}$)[A-Za-z]+(?:[\'\s-][A-Za-z]+)* [A-Za-z]+(?:[\'\s-][A-Za-z]+)*$'
    name_validator = RegexValidator(
    regex=name_regex,
    message='Enter both names, no special characters'
)
    
    gender_choices = [('Male', 'Male'), 
    ('Female', 'Female')]

    name = models.CharField(max_length=100, validators= [name_validator])
    user_number = models.IntegerField(null=False, blank=False, unique=True)
    NIN = models.CharField(max_length=14, unique=True)
    contact = models.CharField(max_length=13, validators=[MinLengthValidator(10), contact_validator])
    email = models.EmailField(null=False, blank=False, unique=True)
    profile_photo = models.ImageField(null=False, blank=False, upload_to='uploads')
    location = models.CharField(max_length=100)
    gender = models.CharField(choices=gender_choices, max_length=10)
    next_of_kin = models.CharField(max_length=100, validators=[name_validator])
    date_of_registration = models.DateField(null=False, blank=False, default=datetime.now)

    def __str__(self):
        return self.name
    

class Save(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False, related_name='member')
    amount = models.PositiveIntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(10000)])
    save_time = models.TimeField(null=False, blank=False, default=datetime.now)
    identity = models.UUIDField(null=False, blank=True, default=uuid.uuid4, unique=True)

    def __str__(self):
        return str(self.member) 