# Generated by Django 3.2.14 on 2022-07-24 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20220724_0253'),
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='people.person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='commerce.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='sale_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='commerce.salepoint', verbose_name='sale point'),
        ),
    ]
