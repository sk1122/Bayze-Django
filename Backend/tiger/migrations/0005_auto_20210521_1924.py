# Generated by Django 3.2.3 on 2021-05-21 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiger', '0004_accesstokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpages',
            name='page_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='facebookpages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
