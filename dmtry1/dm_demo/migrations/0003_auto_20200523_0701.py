# Generated by Django 2.1.4 on 2020-05-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dm_demo', '0002_achievement_brief_tab_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholar_brief_intro_tab',
            name='user_id',
        ),
        migrations.AddField(
            model_name='scholar_brief_intro_tab',
            name='scholar_id',
            field=models.IntegerField(default=0),
        ),
    ]
