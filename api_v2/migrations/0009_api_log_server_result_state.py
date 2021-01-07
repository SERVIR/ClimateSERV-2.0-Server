# Generated by Django 3.0.7 on 2020-07-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v2', '0008_api_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_log',
            name='server_result_state',
            field=models.CharField(default='UNSET', help_text="What was the server's result of this endpoint call.  This value will usually be 'success' or 'error'.  In rare cases this may be set to 'UNSET' or 'UNKNOWN' ", max_length=30, verbose_name='Result of the API Request'),
        ),
    ]
