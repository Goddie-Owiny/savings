from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid


# Create your models here.
# registering a new member to the group
class Member(models.Model):
    contact_regex = r'^(\+256|0)\d{9}$'  # Regex for contact
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
    NIN = models.CharField(max_length=14, unique=True, db_index=True)
    contact = models.CharField(max_length=13, validators=[MinLengthValidator(10), contact_validator])
    email = models.EmailField(null=False, blank=False, unique=True)
    profile_photo = models.ImageField(null=False, blank=False, upload_to='uploads')
    location = models.CharField(max_length=100)
    gender = models.CharField(choices=gender_choices, max_length=10)
    next_of_kin = models.CharField(max_length=100, validators=[name_validator])
    date_of_registration = models.DateField(null=False, blank=True, auto_now_add=True)

    def __str__(self):
        return self.name
    
# user saving money
class Save(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False, related_name='member')
    user_number = models.IntegerField(null=False, blank=False)
    amount = models.PositiveIntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(10000)])
    save_time = models.TimeField(null=False, blank=False, auto_now_add=True)
    identity = models.UUIDField(null=False, blank=True, default=uuid.uuid4, unique=True)

    def __str__(self):
        return str(self.member) 
    

# giving out loans
class Loan(models.Model):
    reciever = models.ForeignKey(Save, on_delete=models.CASCADE, null=False, blank=False)
    amount_borrowed = models.PositiveIntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(10000)])
    witness = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False)
    loan_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)

    def __str__(self):
        return str(self.amount_borrowed)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created
            self.loan_date = timezone.now()  # Set the current date and time
        super().save(*args, **kwargs)