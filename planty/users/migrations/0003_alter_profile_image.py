# Generated by Django 4.0.4 on 2022-06-03 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_name_remove_profile_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(
                default='default-profile-picture.jpg', upload_to='profile_pictures'),
        ),
    ]
