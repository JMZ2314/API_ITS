# Generated by Django 4.1.6 on 2023-02-25 11:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='reference',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
