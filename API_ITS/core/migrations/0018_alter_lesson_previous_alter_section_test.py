# Generated by Django 4.1.6 on 2023-03-20 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_test_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='previous',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.lesson'),
        ),
        migrations.AlterField(
            model_name='section',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.test'),
        ),
    ]
