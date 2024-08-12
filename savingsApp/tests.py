from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Member

class MemberModelTestCase(TestCase):
    def setUp(self):
        """ Set up valid member data for tests """
        self.valid_member_data = {
            'name': 'John Doe',
            'user_number': 88,
            'NIN': '1234567H901234',
            'contact': '+256701234567',
            'email': 'john@example.com',
            'profile_photo': 'path/to/photo.jpg',  # In actual tests, use a mock or a test image file.
            'location': 'Kampala',
            'gender': 'Male',
            'next_of_kin': 'Jane Doe',
        }

    def test_member_creation_valid(self):
        """ Test creating a member with valid data """
        member = Member.objects.create(**self.valid_member_data)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(member.name, 'John Doe')
        self.assertEqual(member.contact, '+256701234567')

    def test_contact_validation_valid(self):
        """ Test that a valid contact does not raise a validation error """
        member = Member(**self.valid_member_data)
        try:
            member.full_clean()  # This should not raise an exception
        except ValidationError:
            self.fail('ValidationError raised for a valid contact number')

    def test_contact_validation_invalid(self):
        """ Test invalid contact should raise a ValidationError """
        invalid_contacts = [
            '25670123456',    # Incorrect length (country code missing)
            '+2567012345x7',  # Contains letters
            '1234567890',     # Missing country code
            '+2567012345678', # Too long
        ]
        for contact in invalid_contacts:
            with self.assertRaises(ValidationError):
                member = Member(contact=contact, **{k: v for k, v in self.valid_member_data.items() if k != 'contact'})
                member.full_clean()  # This should raise ValidationError

    def test_name_validation_valid(self):
        """ Test that a valid name does not raise a validation error """
        member = Member(**self.valid_member_data)
        try:
            member.full_clean()  # This should not raise an exception
        except ValidationError:
            self.fail('ValidationError raised for a valid name')

    def test_name_validation_invalid(self):
        """ Test invalid names should raise a ValidationError """
        invalid_names = [
            'John',         # Missing last name
            'John123 Doe',  # Contains numbers
            'John! Doe',    # Contains special characters
            'JohnDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe Doe',  # Too long
        ]
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                member = Member(name=name, **{k: v for k, v in self.valid_member_data.items() if k != 'name'})
                member.full_clean()  # This should raise ValidationError

