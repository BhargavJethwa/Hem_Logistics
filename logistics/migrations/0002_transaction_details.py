# Generated by Django 3.2.2 on 2021-06-20 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='Details',
            field=models.CharField(default='Advance', max_length=50),
            preserve_default=False,
        ),
    ]
