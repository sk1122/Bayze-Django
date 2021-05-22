# Generated by Django 3.2.3 on 2021-05-21 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tiger', '0008_alter_facebookpages_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookpages',
            name='user',
        ),
        migrations.AddField(
            model_name='facebookpages',
            name='user_fb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fb_user', to=settings.AUTH_USER_MODEL),
        ),
    ]