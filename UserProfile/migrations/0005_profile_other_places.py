# Generated by Django 2.2 on 2019-06-17 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0004_auto_20190617_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='other_places',
            field=models.TextField(default='None'),
            preserve_default=False,
        ),
    ]
