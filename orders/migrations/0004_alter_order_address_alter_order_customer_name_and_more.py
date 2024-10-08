# Generated by Django 5.1 on 2024-08-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_preferred_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(
                blank=True, default="", max_length=200, verbose_name="Комментарий"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="customer_name",
            field=models.CharField(
                blank=True, default="", max_length=50, verbose_name="Имя"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.CharField(
                blank=True, default="", max_length=30, verbose_name="Почта"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone_number",
            field=models.CharField(
                blank=True, default="", max_length=20, verbose_name="Номер телефона"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=8, verbose_name="Цена"
            ),
        ),
    ]
