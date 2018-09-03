# Generated by Django 2.0.8 on 2018-09-03 10:08

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_roles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roleassignment',
            options={'ordering': ['period']},
        ),
        migrations.AlterField(
            model_name='role',
            name='legacy_id',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='role',
            name='legacy_table',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='legacy_end_id',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='legacy_start_id',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='legacy_table',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='role',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_assignments', to='people.Role', verbose_name='role'),
        ),
    ]
