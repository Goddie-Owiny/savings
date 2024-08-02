from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Member, Save, Loan

class MemberViewsTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Setup code to create necessary objects for tests
        cls.client = Client()
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.client.login(username='testuser', password='password')
        
        cls.member = Member.objects.create(
            name='John Doe',
            user_number=1,
            NIN='12345678901234',
            contact='+256701234567',
            email='john@example.com',
            profile_photo='path/to/photo.jpg',
            location='Kampala',
            gender='Male',
            next_of_kin='Jane Doe',
        )
        
        cls.save = Save.objects.create(
            member=cls.member,
            amount=10000,
            save_time='12:00:00'
        )
        
        cls.loan = Loan.objects.create(
            reciever=cls.save,
            amount_borrowed=5000,
            witness=cls.member,
            loan_date='2024-08-01T12:00:00Z'
        )
        
    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'savingsApp/dashboard.html')
        self.assertContains(response, 'John Doe')

    def test_mem_reg_view(self):
        data = {
            'name': 'Jane Doe',
            'user_number': 2,
            'NIN': '98765432109876',
            'contact': '+256702345678',
            'email': 'jane@example.com',
            'profile_photo': 'path/to/photo.jpg',
            'location': 'Entebbe',
            'gender': 'Female',
            'next_of_kin': 'John Doe',
        }
        response = self.client.post(reverse('mem_reg'), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Member.objects.filter(name='Jane Doe').exists())

    def test_save_view(self):
        data = {'amount': 5000}
        response = self.client.post(reverse('save', args=[self.save.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.save.refresh_from_db()
        self.assertEqual(self.save.amount, 15000)

    def test_loan_view(self):
        data = {
            'reciever': self.save.id,
            'amount_borrowed': 2000,
            'witness': self.member.id,
            'loan_date': '2024-08-01T12:00:00Z'
        }
        response = self.client.post(reverse('loan'), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Loan.objects.filter(amount_borrowed=2000).exists())

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('login'))