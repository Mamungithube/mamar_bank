from django import forms
from .models import Transaction
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') 
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput() 

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_diposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_diposit_amount:
            raise forms.validation_errors(
                f'Your amount is too low ,you amount must be between"{min_diposit_amount}'
            )
        return amount

from django import forms

class WithdrawForm(TransactionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assuming 'balance' is an attribute of the form instance
        self.balance = 1000  # Replace with the actual balance value

    def clean_amount(self):
        min_withdraw_amount = 100
        max_deposit_amount = 20000
        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f"Your amount is too low, it must be between {min_withdraw_amount}."
            )
        if amount > max_deposit_amount:
            raise forms.ValidationError(
                f"Your amount is too high, it must be between {max_deposit_amount}."
            )
        if amount > self.balance:
            raise forms.ValidationError(
                f"Your balance is not enough, it must be less than {self.balance}."
            )

        return amount

    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return amount