# Generated by Django 3.1.7 on 2021-06-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210620_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
