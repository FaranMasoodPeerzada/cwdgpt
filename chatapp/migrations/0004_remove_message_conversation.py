# Generated by Django 4.2.4 on 2023-08-21 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_rename_message_message_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
    ]