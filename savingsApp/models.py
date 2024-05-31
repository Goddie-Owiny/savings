from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator


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

    name = models.CharField(max_length=100, validators= [name_validator])
    user_number = models.IntegerField(null=False, blank=False, unique=True)
    NIN = models.CharField(max_length=14, unique=True)
    contact = models.CharField(max_length=13, validators=[MinLengthValidator(10), contact_validator])
    email = models.EmailField(null=False, blank=False)
    profile_photo = models.ImageField(null=False, blank=False, upload_to='uploads')
    location = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)

    def __str__(self):
        return self.name