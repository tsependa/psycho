# Generated by Django 2.2.1 on 2019-05-31 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0023_supportquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.TextField(blank=True, null=True)),
                ('question', models.TextField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
