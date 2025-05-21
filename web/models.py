from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

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
    # Убрано поле owner, чтобы категории не были привязаны к пользователю
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