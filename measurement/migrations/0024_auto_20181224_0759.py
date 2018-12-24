# Generated by Django 2.1.4 on 2018-12-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0023_auto_20181223_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_correlation',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_max',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_mean',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_min',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_skewness',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='doc_std_deviation',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True),
        ),
    ]