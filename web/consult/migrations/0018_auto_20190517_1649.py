# Generated by Django 2.2.1 on 2019-05-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0017_specialist_avatar_mob'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialist',
            options={'ordering': ('promo',)},
        ),
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='payment',
            name='payload',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='yandex_payment',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]