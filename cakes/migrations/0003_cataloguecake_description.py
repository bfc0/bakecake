# Generated by Django 5.1 on 2024-08-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0002_cartaddition_order_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='cataloguecake',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
    ]
