# Generated by Django 3.1 on 2023-01-02 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230101_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
