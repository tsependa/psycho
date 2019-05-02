# Generated by Django 2.1.7 on 2019-05-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0014_auto_20190418_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True)),
                ('answer', models.TextField(blank=True)),
                ('sequence', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='specialist',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default='female', max_length=10),
        ),
    ]
