# Generated by Django 2.2.6 on 2019-10-26 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191024_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='accepted_terms_condition',
            field=models.BooleanField(default=False),
        ),
    ]
