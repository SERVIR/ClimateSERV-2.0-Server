# Generated by Django 2.2.2 on 2020-06-28 23:15

import common_utils.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ETL_Dataset',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=common_utils.utils.get_Random_String_UniqueID_20Chars, editable=False, max_length=40)),
                ('dataset_name', models.CharField(default='Unknown Dataset Name', help_text='A Human Readable Custom Name to identify this dataset.  Typically expected usage would be for Admin to set this name so they can quickly understand which data set they are looking at.  They could also use the other TDS fields to understand exactly which dataset this refers to.', max_length=90, verbose_name='Human Readable Dataset Short Name')),
                ('is_pipeline_enabled', models.BooleanField(default=False, help_text="Is this ETL Dataset currently set to 'enabled' for ETL Pipeline processing?  If this is set to False, then when the ETL job runs to process this incoming data, the ETL pipeline for this process will be stopped before it makes an attempt.  This is intended as a way for admin to just 'turn off' or 'turn on' a specific ETL job that has been setup.")),
                ('is_pipeline_active', models.BooleanField(default=False, help_text='Is this ETL Dataset currently being run through the ETL Pipeline? If this is set to True, that means an ETL job is actually running for this specific dataset and data ingestion is currently in progress.  When a pipeline finishes (success or error) this value should be set to False by the pipeline code.')),
                ('capabilities', models.TextField(default='{}', help_text="Set Automatically by ETL Pipeline.  Please don't touch this!  Messing with this will likely result in broken content elsewhere in the system.  This is a field to hold Dataset specific information that the clientside code may need access to in order to properly render the details from this dataset.  (In ClimateSERV 1.0, some of this was a GeoReference, Time/Date Ranges, and other information.)", verbose_name='JSON Data')),
                ('tds_product_name', models.CharField(default='UNKNOWN_PRODUCT_NAME', help_text="The Product name as defined on the THREDDS Data Server (TDS) Conventions Document.  Example Value: 'EMODIS-NDVI'", max_length=90, verbose_name='(TDS Conventions) Product Name')),
                ('tds_region', models.CharField(default='UNKNOWN_REGION', help_text="The Region as defined on the THREDDS Data Server (TDS) Conventions Document.  Example Value: 'Global'", max_length=90, verbose_name='(TDS Conventions) Region')),
                ('tds_spatial_resolution', models.CharField(default='UNKNOWN_SPATIAL_RESOLUTION', help_text="The Spatial Resolution as defined on the THREDDS Data Server (TDS) Conventions Document.  Example Value: '250m'", max_length=90, verbose_name='(TDS Conventions) Spatial Resolution')),
                ('tds_temporal_resolution', models.CharField(default='UNKNOWN_TEMPORAL_RESOLUTION', help_text="The Temporal Resolution as defined on the THREDDS Data Server (TDS) Conventions Document.  Example Value: '2mon'", max_length=90, verbose_name='(TDS Conventions) Temporal Resolution')),
                ('additional_json', models.TextField(default='{}', help_text="Extra data field.  Please don't touch this!  Messing with this will likely result in broken content elsewhere in the system.", verbose_name='JSON Data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('created_by', models.CharField(default='Table_Default_Process', help_text='Who or What Process created this record? 90 chars max', max_length=90, verbose_name='Created By User or Process Name or ID')),
                ('is_test_object', models.BooleanField(default=False, help_text='Is this Instance meant to be used ONLY for internal platform testing? (Used only for easy cleanup - DO NOT DEPEND ON FOR VALIDATION)')),
            ],
        ),
        migrations.CreateModel(
            name='ETL_Granule',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=common_utils.utils.get_Random_String_UniqueID_20Chars, editable=False, max_length=40)),
                ('granule_name', models.CharField(default='Unknown Granule Name', help_text="Most of the time, this may be a filename.  Sometimes it is not.  It should be a name that is unique to the combination of dataset and temporal data value.  This row should be useful in tracking down the specific granule's file/source info.", max_length=250, verbose_name='Granule Name')),
                ('granule_contextual_information', models.TextField(default='No Additional Information', help_text='A way to capture additional contextual information around a granule, if needed.', verbose_name='Granule Contextual Information')),
                ('etl_dataset_uuid', models.CharField(default='UNSET_DATASET_UUID', help_text='Each Individual Granule has a parent ETL Dataset, storing the association here', max_length=40, verbose_name='ETL Dataset UUID')),
                ('is_missing', models.BooleanField(default=False, help_text='Was this expected granule missing at the time of processing?  If this is set to True, that means during an ingest run, there was an expected granule that was either not found at the data source, or had an error that made it unable to be processed and ingested.  The time that this record gets created as compared to ETL Log rows would be a good way to nail down the exact issue as more data is stored about issues in the ETL Log table.')),
                ('additional_json', models.TextField(default='{}', help_text="Extra data field.  Please don't touch this!  Messing with this will likely result in broken content elsewhere in the system.", verbose_name='JSON Data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('created_by', models.CharField(default='Table_Default_Process', help_text='Who or What Process created this record? 90 chars max', max_length=90, verbose_name='Created By User or Process Name or ID')),
                ('is_test_object', models.BooleanField(default=False, help_text='Is this Instance meant to be used ONLY for internal platform testing? (Used only for easy cleanup - DO NOT DEPEND ON FOR VALIDATION)')),
            ],
        ),
        migrations.CreateModel(
            name='ETL_Log',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=common_utils.utils.get_Random_String_UniqueID_20Chars, editable=False, max_length=40)),
                ('activity_event_type', models.CharField(default='Unknown ETL Activity Event Type', help_text='What is the standardized type for this ETL Activity Event?', max_length=90, verbose_name='Standardized Activity Event Type')),
                ('activity_description', models.TextField(default='No Description', help_text='A field for more detailed information on an ETL Event Activity', verbose_name='Activity Description')),
                ('etl_dataset_uuid', models.CharField(default='UNSET_DATASET_UUID', help_text='If there is an associated ETL Dataset UUID, it should appear here.  Note: This field may be blank or unset, not all events will have one of these associated items.', max_length=40, verbose_name='ETL Dataset UUID')),
                ('etl_granule_uuid', models.CharField(default='UNSET_GRANULE_UUID', help_text='If there is an associated ETL Granule UUID, it should appear here.  Note: This field may be blank or unset, not all events will have one of these associated items.', max_length=40, verbose_name='ETL Granule UUID')),
                ('is_alert', models.BooleanField(default=False, help_text='Is this an Item that should be considered an alert?  (by default, all errors and warnings are considered alerts)')),
                ('is_alert_dismissed', models.BooleanField(default=False, help_text='Setting this to True will change the display style for the admin.')),
                ('additional_json', models.TextField(default='{}', help_text="Extra data field.  Please don't touch this!  Messing with this will likely result in broken content elsewhere in the system.", verbose_name='JSON Data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('created_by', models.CharField(default='Table_Default_Process', help_text='Who or What Process created this record? 90 chars max', max_length=90, verbose_name='Created By User or Process Name or ID')),
                ('is_test_object', models.BooleanField(default=False, help_text='Is this Instance meant to be used ONLY for internal platform testing? (Used only for easy cleanup - DO NOT DEPEND ON FOR VALIDATION)')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_id',
            field=models.CharField(default='UNKNOWN_AUTH_ID', max_length=40),
        ),
    ]
