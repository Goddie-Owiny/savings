from . models import *
from django.forms import ModelForm
from django import forms


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class SavingsForm(ModelForm):
    class Meta: 
        model = Save
        fields = ['member', 'amount', 'save_time']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['reciever', 'amount_borrowed', 'witness', 'loan_date']




        # saved = Save.objects.get('amount')
    def clean_amount_borrowed(self):
        amount_borrowed = self.cleaned_data.get('amount_borrowed')
        if amount_borrowed <= 10000:
            raise forms.ValidationError('You can only borrow 10000 or greater.')
        return amount_borrowed

    def clean(self):
        cleaned_data = super().clean()
        reciever = cleaned_data.get('reciever')
        witness = cleaned_data.get('witness')

        if reciever == witness:
            raise forms.ValidationError("The receiver can't be a witness.")
        
        # Add more custom validation here if necessary

        return cleaned_data