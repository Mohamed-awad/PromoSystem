# Generated by Django 3.1.1 on 2020-10-03 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promoApplication', '0003_auto_20200930_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]