from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


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
    event = models.ForeignKey(Event,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='cakes',
                              verbose_name='Повод')
    description = models.TextField(blank=True,
                                   null=False,
                                   default='',
                                   verbose_name='Описание')
    price = models.FloatField(blank=False,
                              null=False,
                              verbose_name='Цена')

    image = models.ImageField(blank=True,
                              null=True,
                              verbose_name='Изображение',
                              upload_to="static/img")

    class Meta:
        verbose_name = 'Готовый торт'
        verbose_name_plural = 'Готовые торты'

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'name': self.name,
            'event': self.event if self.event else '',
            'description': self.description,
            'price': self.price,
            'image_url': self.image.url if self.image else None,
        }


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
        return f"Кастомный торт #{self.id}"

    def serialize(self):
        return {
            "name": str(self),
            "price": self.price,
            "title": self.title if self.title else "Без надписи",
            "level": self.level.name,
            "shape": self.shape.name,
            "topping": self.topping.name,
            "berry": self.berry.name,
            "decoration": self.decoration.name,
        }


def adjust_cake_price(cake, desired_dt):
    if desired_dt.tzinfo is None:
        desired_dt = timezone.make_aware(
            desired_dt, timezone.get_current_timezone())
    if desired_dt <= timezone.now() + timedelta(hours=24):
        cake.price *= 1.2
        cake.save()


class Visit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    session_key = models.CharField(max_length=40)
    timestamp = models.DateTimeField(default=timezone.now)


class CartAddition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    session_key = models.CharField(max_length=40)
    product_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    session_key = models.CharField(max_length=40)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
