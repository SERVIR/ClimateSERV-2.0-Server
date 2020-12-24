# Generated by Django 3.0.7 on 2020-07-26 20:36

import common_utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v2', '0005_etl_pipelinerun'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available_Granule',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=common_utils.utils.get_Random_String_UniqueID_20Chars, editable=False, max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('created_by', models.CharField(default='Table_Default_Process', help_text='Who or What Process created this record? 90 chars max', max_length=90, verbose_name='Created By User or Process Name or ID')),
                ('additional_json', models.TextField(default='{}', help_text="Extra data field.  Please don't touch this!  Messing with this will likely result in broken content elsewhere in the system.", verbose_name='JSON Data')),
                ('is_test_object', models.BooleanField(default=False, help_text='Is this Instance meant to be used ONLY for internal platform testing? (Used only for easy cleanup - DO NOT DEPEND ON FOR VALIDATION)')),
            ],
        ),
    ]
