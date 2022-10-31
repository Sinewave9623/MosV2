# Generated by Django 3.2.16 on 2022-10-31 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20221029_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermaster',
            old_name='phoneNumber',
            new_name='contactNo',
        ),
        migrations.RenameField(
            model_name='customermaster',
            old_name='registrationDate',
            new_name='registration_Date',
        ),
        migrations.RenameField(
            model_name='customermaster',
            old_name='swCustomerId',
            new_name='sw_CustomerId',
        ),
        migrations.RenameField(
            model_name='customermaster',
            old_name='valid_date',
            new_name='valid_Date',
        ),
        migrations.RenameField(
            model_name='membermaster',
            old_name='phoneNumber',
            new_name='contactNo',
        ),
        migrations.RenameField(
            model_name='membermaster',
            old_name='email',
            new_name='emailId',
        ),
        migrations.AddField(
            model_name='customermaster',
            name='emailId',
            field=models.EmailField(blank=True, max_length=40, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customermaster',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customermaster',
            name='photo',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='customer_photo'),
        ),
    ]