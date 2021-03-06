# Generated by Django 2.1.2 on 2018-11-02 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20181102_0528'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStageReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='2018-11-02', max_length=200)),
                ('funding', models.IntegerField(blank=True, default=0, null=True, verbose_name='Funding')),
                ('has_customers', models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], null=True)),
                ('revenue', models.IntegerField(blank=True, default=0, null=True, verbose_name='Revenue')),
                ('fulltime_employees', models.IntegerField(blank=True, default=0, null=True, verbose_name='Fulltime Employees')),
                ('date_updated', models.DateField(verbose_name='Date updated')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Company')),
                ('investor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.Investor')),
                ('product_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.ProductStage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='Stage',
            new_name='MasterStage',
        ),
        migrations.RemoveField(
            model_name='companyreport',
            name='company',
        ),
        migrations.RemoveField(
            model_name='companyreport',
            name='investor',
        ),
        migrations.RemoveField(
            model_name='companyreport',
            name='stage_ptr',
        ),
        migrations.DeleteModel(
            name='CompanyReport',
        ),
    ]
