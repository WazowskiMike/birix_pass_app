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

    # Убедимся, что поле не обязательное
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].required = False

class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ['title', 'card_number', 'full_name', 'expiry_date', 'cvv', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']