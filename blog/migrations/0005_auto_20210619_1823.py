# Generated by Django 3.1.7 on 2021-06-19 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default='avatar.png', upload_to='blog_pics/%Y/%m/%d/'),
        ),
    ]
