# Generated by Django 2.1.2 on 2018-11-02 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_auto_20181102_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='companystagereport',
            name='stage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='data.MasterStage'),
            preserve_default=False,
        ),
    ]
