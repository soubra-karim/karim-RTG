# Generated by Django 4.2.5 on 2024-02-24 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0010_remove_jobtoclusters_job_posting_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobToClusters',
        ),
    ]
