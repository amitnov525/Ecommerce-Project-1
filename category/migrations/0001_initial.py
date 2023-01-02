# Generated by Django 3.1 on 2023-01-01 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=355)),
                ('cat_img', models.ImageField(blank=True, upload_to='photos/category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
