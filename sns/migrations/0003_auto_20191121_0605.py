# Generated by Django 2.2.7 on 2019-11-20 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0002_message_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='group',
            field=models.ForeignKey(default='public', on_delete=django.db.models.deletion.CASCADE, to='sns.Group'),
        ),
    ]