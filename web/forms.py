from django import forms
from .models import Entry, Category, BankCard

class MasterLoginForm(forms.Form):
    master_password = forms.CharField(
        label='Мастер-пароль',
        widget=forms.PasswordInput,
    )

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'username', 'password', 'url', 'notes', 'category']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].required = False

class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = [
            'title', 'card_number', 'full_name', 'expiry_date', 'cvv',
            'description', 'category', 'is_payment', 'routing_number', 'account_number'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card_number'].required = False
        self.fields['full_name'].required = False
        self.fields['expiry_date'].required = False
        self.fields['cvv'].required = False
        self.fields['description'].required = False
        self.fields['routing_number'].required = False
        self.fields['account_number'].required = False

    def clean_card_number(self):
        number = self.cleaned_data.get('card_number')
        if not number:
            return None
        return number.replace(' ', '')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']