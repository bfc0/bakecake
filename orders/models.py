from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from account.models import CustomUser


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
                                     related_name="order_contenttype",
                                     limit_choices_to={"model__in":
                                                       ("cataloguecake",
                                                        "customcake")})
    object_id = models.PositiveIntegerField(verbose_name='ID торта')
    content_object = GenericForeignKey("content_type", "object_id")

    customer = models.ForeignKey(CustomUser,
                                 blank=False,
                                 null=False,
                                 on_delete=models.CASCADE,
                                 related_name='customer_orders',
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
