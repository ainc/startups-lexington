# Generated by Django 2.1.2 on 2018-11-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20181101_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='has_customers',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], null=True),
        ),
    ]
