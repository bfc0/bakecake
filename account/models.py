from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Необходимо ввести номер телефона")
        if not password:
            password = "12345"  # Чтобы не отправлять по почте

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField("Телефон", unique=True, db_index=True)
    name = models.CharField("Имя", max_length=30, blank=True)
    email = models.EmailField("Почта", blank=True, null=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)

    def save(self, *args, **kwargs):
        if self.email:
            if CustomUser.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "Пользователь с таким почтовым адресом уже существует")

        super().save(*args, **kwargs)
