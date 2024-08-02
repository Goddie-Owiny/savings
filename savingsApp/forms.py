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
        fields = ['member', 'amount']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['reciever', 'amount_borrowed', 'witness']



        # saved = Save.objects.get('amount')
    def clean_amount_borrowed(self):
        amount_borrowed = self.cleaned_data.get('amount_borrowed')
        if amount_borrowed < 10000:
            raise forms.ValidationError('You can only borrow Ugx.10000 or more.')
        return amount_borrowed

    def clean(self):
        cleaned_data = super().clean()
        reciever = cleaned_data.get('reciever')
        witness = cleaned_data.get('witness')

        if reciever and witness and reciever.user_number == witness.user_number:
            raise forms.ValidationError("The receiver can't be the same person as the witness.")

        # Add more custom validation here if necessary

        return cleaned_data
    
    def clean_amount_borrowed(self):
        amount_borrowed = self.cleaned_data['amount_borrowed']
        reciever = self.cleaned_data['reciever']
        if amount_borrowed > reciever.amount:
            raise forms.ValidationError('Cannot borrow more than the amount saved.')
        return amount_borrowed