# Generated by Django 2.0.9 on 2018-12-20 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rnames_app', '0014_auto_20181220_1319'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='qualifier',
            unique_together={('qualifier_name', 'stratigraphic_qualifier')},
        ),
    ]