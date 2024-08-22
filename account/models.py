from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Необходимо ввести номер телефона")
        if not password:
            password = "12345"

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


class Event(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Название')

    class Meta:
        verbose_name = 'Повод'
        verbose_name_plural = 'Поводы'

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Количество уровней')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Количество уровней'
        verbose_name_plural = 'Количество уровней'

    def __str__(self):
        return self.name


class Shape(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Форма')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Топпинг')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.name


class Berry(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Ягоды')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Ягоды'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.name


class Decoration(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Декор')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    class Meta:
        verbose_name = 'Декор'
        verbose_name_plural = 'Декор'

    def __str__(self):
        return self.name


class CatalogueCake(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Название')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')
    event = models.ForeignKey(Event,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='cakes',
                              verbose_name='Повод')
    image = models.ImageField(blank=True,
                              null=True,
                              verbose_name='Изображение',
                              upload_to='media')

    class Meta:
        verbose_name = 'Готовый торт'
        verbose_name_plural = 'Готовые торты'

    def __str__(self):
        return self.name


class CustomCake(models.Model):
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')
    title = models.TextField(blank=True,
                             null=False,
                             default='',
                             verbose_name='Надпись')
    level = models.ForeignKey(Level,
                              blank=False,
                              null=False,
                              on_delete=models.CASCADE,
                              related_name='cakes',
                              verbose_name='Количество уровней')
    shape = models.ForeignKey(Shape,
                              blank=False,
                              null=False,
                              on_delete=models.CASCADE,
                              related_name='cakes',
                              verbose_name='Форма')
    topping = models.ForeignKey(Topping,
                                blank=False,
                                null=False,
                                on_delete=models.CASCADE,
                                related_name='cakes',
                                verbose_name='Топпинг')
    berry = models.ForeignKey(Berry,
                              blank=False,
                              null=False,
                              on_delete=models.CASCADE,
                              related_name='cakes',
                              verbose_name='Ягоды')
    decoration = models.ForeignKey(Decoration,
                                   blank=False,
                                   null=False,
                                   on_delete=models.CASCADE,
                                   related_name='cakes',
                                   verbose_name='Декор')

    class Meta:
        verbose_name = 'Кастомный торт'
        verbose_name_plural = 'Кастомные торты'

    def __str__(self):
        return f"Кастомный торт {self.id}"


class OrderStatus(models.Model):
    name = models.TextField(blank=False,
                            null=False,
                            verbose_name='Название')

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

    def __str__(self):
        return self.name


class Order(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     verbose_name='Тип торта',
                                     limit_choices_to={"model__in":
                                                       ("cataloguecake",
                                                        "customcake")})
    object_id = models.PositiveIntegerField(verbose_name='ID торта')
    content_object = GenericForeignKey("content_type", "object_id")

    customer = models.ForeignKey(CustomUser,
                                 blank=False,
                                 null=False,
                                 on_delete=models.CASCADE,
                                 related_name='ordrs',
                                 verbose_name='Клиент')
    status = models.ForeignKey(OrderStatus,
                               blank=False,
                               null=False,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Статус')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')
    comment = models.TextField(blank=True,
                               null=False,
                               default='',
                               verbose_name='Комментарий')
    address = models.TextField(blank=True,
                               null=False,
                               default='',
                               verbose_name='Комментарий')
    customer_name = models.TextField(blank=True,
                                     null=False,
                                     default='',
                                     verbose_name='Имя')
    phone_number = models.TextField(blank=True,
                                    null=False,
                                    default='',
                                    verbose_name='Номер телефона')
    email = models.TextField(blank=True,
                             null=False,
                             default='',
                             verbose_name='Почта')
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Создано')
    date_modified = models.DateTimeField(blank=True,
                                         null=True,
                                         auto_now=True,
                                         verbose_name='Изменено')
    date_delivered = models.DateTimeField(blank=True,
                                          null=True,
                                          verbose_name='Доставлено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Заказ #{self.id}"
