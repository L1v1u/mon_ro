# Generated by Django 2.2.6 on 2019-10-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
