# Generated by Django 2.0.5 on 2018-05-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_goods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='id',
        ),
        migrations.AlterField(
            model_name='goods',
            name='productid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]