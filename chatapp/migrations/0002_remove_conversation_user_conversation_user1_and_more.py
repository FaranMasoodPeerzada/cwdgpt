# Generated by Django 4.2.4 on 2023-08-20 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='user',
        ),
        migrations.AddField(
            model_name='conversation',
            name='user1',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversation',
            name='user2',
            field=models.ForeignKey(default=232, on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user2', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='response',
            field=models.TextField(default='helo'),
        ),
    ]
