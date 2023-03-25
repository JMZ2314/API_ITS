# Generated by Django 4.1.6 on 2023-03-24 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
        ('sections', '0002_remove_section_test'),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='review_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.lesson'),
        ),
        migrations.AddField(
            model_name='test',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sections.section'),
        ),
    ]
