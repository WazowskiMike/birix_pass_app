from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import re

class MasterConfig(models.Model):
    """
    Хранит единственный объект с мастер-паролем.
    """
    # Храним хэш пароля
    password_hash = models.CharField(max_length=128, blank=False)

    @classmethod
    def load(cls):
        """
        Возвращает единственный экземпляр MasterConfig.
        Если его ещё нет — создаёт с рандомным паролем
        (или пустым хэшем), чтобы гарантировать наличие записи.
        """
        try:
            return cls.objects.get()
        except ObjectDoesNotExist:
            # Создаём запись с пустым паролем
            instance = cls(password_hash=make_password(get_random_string()))
            instance.save()
            return instance

    def check_password(self, raw_password: str) -> bool:
        """Проверяет сырой пароль против хэша."""
        return check_password(raw_password, self.password_hash)

    def set_password(self, raw_password: str):
        """Устанавливает (хэширует) новый пароль."""
        self.password_hash = make_password(raw_password)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Entry(models.Model):
    category = models.ForeignKey(Category, related_name='entries', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class BankCard(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='bank_cards',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', self.expiry_date):
            raise ValidationError("Неверный формат даты. Используйте MM/YY.")

    def __str__(self):
        return f"{self.title} - ****{self.card_number[-4:]}"