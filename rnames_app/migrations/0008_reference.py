# Generated by Django 2.0.9 on 2018-12-05 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rnames_app', '0007_auto_20181206_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Deleted'), (0, 'Active')], default=0, help_text='Is the record deleted')),
                ('title', models.CharField(help_text='Enter the title of the reference', max_length=200)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createdby_reference', to=settings.AUTH_USER_MODEL, verbose_name='The user that is automatically assigned')),
                ('modified_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modifiedby_reference', to=settings.AUTH_USER_MODEL, verbose_name='The user that is automatically assigned')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
