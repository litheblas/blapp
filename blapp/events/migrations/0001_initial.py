# Generated by Django 3.2.7 on 2022-01-22 12:55

import blapp.utils.db_fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', blapp.utils.db_fields.PrimaryKeyUUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', blapp.utils.db_fields.NameField(max_length=256, verbose_name='event name')),
                ('event_description', blapp.utils.db_fields.DescriptionField(blank=True, verbose_name='description')),
                ('published', models.BooleanField(default=True)),
                ('obligatory', models.BooleanField(default=True, verbose_name='obligatory attendance')),
                ('starts', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date')),
                ('ends', models.DateTimeField(blank=True, null=True, verbose_name='end date')),
                ('signup_deadline', models.DateTimeField(blank=True, null=True, verbose_name='signup deadline')),
                ('contact_person', models.TextField(blank=True, null=True, verbose_name='contact person information')),
                ('attendants', models.ManyToManyField(related_name='attendants', through='events.Attendance', to='people.Person')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_creator', to='people.person', verbose_name='event creator')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.person'),
        ),
    ]
