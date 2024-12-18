# Generated by Django 5.1 on 2024-12-07 10:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
