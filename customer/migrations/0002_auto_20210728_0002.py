# Generated by Django 3.1.1 on 2021-07-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookappointment',
            name='contact',
            field=models.BigIntegerField(),
        ),
    ]
