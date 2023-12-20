# Generated by Django 4.2.4 on 2023-09-06 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_delegate_hot_key_alter_delegate_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume_24h', models.FloatField(default=0.0)),
                ('current_price', models.FloatField(default=0.0)),
                ('change_24h', models.FloatField(default=0.0)),
                ('circulating_supply', models.FloatField(default=0.0)),
                ('total_stakes', models.FloatField(default=0.0)),
                ('market_cap', models.FloatField(default=0.0)),
                ('total_supply', models.FloatField(default=0.0)),
                ('percent_staked', models.FloatField(default=0.0)),
            ],
        ),
    ]
