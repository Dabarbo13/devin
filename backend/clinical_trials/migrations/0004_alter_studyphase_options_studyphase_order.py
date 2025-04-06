# Generated by Django 5.2 on 2025-04-05 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_trials', '0003_study_indication_study_phase_study_sponsor_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studyphase',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='studyphase',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
