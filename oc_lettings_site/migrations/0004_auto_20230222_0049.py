# Generated by Django 3.0 on 2023-02-22 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0003_auto_20230222_0025"),
    ]

    operations = [
        migrations.RemoveField(model_name="letting", name="address",),
        migrations.RemoveField(model_name="profile", name="user",),
        migrations.DeleteModel(name="Address",),
        migrations.DeleteModel(name="Letting",),
        migrations.DeleteModel(name="Profile",),
    ]
