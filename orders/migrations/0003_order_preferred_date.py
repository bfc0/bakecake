# Generated by Django 5.1 on 2024-08-23 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_order_status_delete_orderstatus"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="preferred_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Предпочтительная дата"
            ),
        ),
    ]
