# Generated by Django 2.2.11 on 2020-03-26 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20200326_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profileicon',
            old_name='icon_url',
            new_name='icon',
        ),
    ]