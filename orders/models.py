from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from account.models import CustomUser


class Order(models.Model):
    STATUS = (
        ('NEW', 'Неоплачен'),
        ('PAY', 'Оплачен'),
        ('ACC', 'Принят'),
        ('PREP', 'Готовится'),
        ('OUT', 'Передан в доставку'),
        ('COMP', 'Выполнен'),
        ('CANC', 'Отменен'),
    )
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

    status = models.CharField(max_length=4, choices=STATUS, default='NEW')
    price = models.DecimalField(blank=False,
                                null=False,
                                max_digits=8,
                                decimal_places=2,
                                verbose_name='Цена')
    comment = models.TextField(blank=True,
                               null=False,
                               default='',
                               verbose_name='Комментарий')
    address = models.CharField(blank=True,
                               null=False,
                               default='',
                               max_length=200,
                               verbose_name='Адрес')
    customer_name = models.CharField(blank=True,
                                     null=False,
                                     default='',
                                     max_length=50,
                                     verbose_name='Имя')
    phone_number = models.CharField(blank=True,
                                    null=False,
                                    default='',
                                    max_length=20,
                                    verbose_name='Номер телефона')
    email = models.CharField(blank=True,
                             null=False,
                             default='',
                             max_length=30,
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
    preferred_date = models.DateTimeField(blank=True,
                                          null=True,
                                          verbose_name='Предпочтительная дата')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Заказ #{self.id}"

    def serialize(self):
        pd = self.preferred_date
        return {
            "id": self.id,
            "cake": self.content_object.serialize(),
            "status": self.get_status_display(),
            "price": str(self.price),
            "phone_number": self.phone_number,
            "customer_name": self.customer_name,
            "address": self.address,
            "comment": self.comment,
            "preferred_date": pd.strftime("%d-%m-%y %H:%M") if pd else "",
        }
