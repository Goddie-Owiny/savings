# Generated by Django 5.0.7 on 2024-08-02 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savingsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='NIN',
            field=models.CharField(db_index=True, max_length=14, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='date_of_registration',
            field=models.DateField(auto_now_add=True),
        ),
    ]
