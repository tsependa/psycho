# Generated by Django 2.2.1 on 2019-05-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0016_auto_20190513_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialist',
            name='avatar_mob',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]