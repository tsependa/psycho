# Generated by Django 2.2.1 on 2019-06-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0028_auto_20190613_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinar',
            name='status',
            field=models.CharField(choices=[('hidden', 'Скрыт'), ('enroll_open', 'Запись открыта'), ('enroll_closed', 'Запись закрыта'), ('ended', 'Завершен')], default='hidden', max_length=20),
        ),
        migrations.RemoveField(
            model_name='webinar',
            name='themes',
        ),
        migrations.AddField(
            model_name='webinar',
            name='themes',
            field=models.TextField(blank=True, null=True),
        ),
    ]