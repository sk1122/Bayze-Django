# Generated by Django 3.2.3 on 2021-05-20 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPages',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('page', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facebook_user', to='socialaccount.socialaccount')),
            ],
        ),
    ]