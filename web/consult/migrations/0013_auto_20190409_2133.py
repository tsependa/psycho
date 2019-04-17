# Generated by Django 2.1.7 on 2019-04-09 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0012_specialist_methods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('sequence', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='specialist',
            name='types',
            field=models.ManyToManyField(blank=True, to='consult.Type'),
        ),
    ]
