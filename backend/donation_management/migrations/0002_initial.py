# Generated by Django 5.2 on 2025-04-05 19:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donation_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chainofcustodylog',
            name='performed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custody_actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donation',
            name='collected_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collected_donations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donationappointment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donation',
            name='appointment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donation', to='donation_management.donationappointment'),
        ),
        migrations.AddField(
            model_name='donationappointment',
            name='donation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_management.donationtype'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_management.donationtype'),
        ),
        migrations.AddField(
            model_name='donor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donationappointment',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_appointments', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='donoreligibilityassessment',
            name='assessed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donor_assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donoreligibilityassessment',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eligibility_assessments', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='donoreligibilityassessment',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_management.donoreligibilityrule'),
        ),
        migrations.AddField(
            model_name='donormedicalhistory',
            name='donor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medical_history', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='labtest',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_tests', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='labtest',
            name='ordered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered_tests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='physicalexam',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physical_exams', to='donation_management.donor'),
        ),
        migrations.AddField(
            model_name='physicalexam',
            name='examiner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conducted_exams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sample',
            name='donation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='donation_management.donation'),
        ),
        migrations.AddField(
            model_name='sample',
            name='processed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_samples', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chainofcustodylog',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custody_logs', to='donation_management.sample'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_management.sampletype'),
        ),
        migrations.AddField(
            model_name='sample',
            name='storage_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='donation_management.storagelocation'),
        ),
        migrations.AddField(
            model_name='storagelocation',
            name='storage_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='donation_management.storageunit'),
        ),
        migrations.AlterUniqueTogether(
            name='donoreligibilityassessment',
            unique_together={('donor', 'rule')},
        ),
        migrations.AlterUniqueTogether(
            name='storagelocation',
            unique_together={('storage_unit', 'position')},
        ),
    ]
