# Generated by Django 3.2.2 on 2021-06-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_auto_20210601_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='Notifications',
            field=models.BooleanField(default=True, verbose_name='Notifications Needed'),
        ),
    ]