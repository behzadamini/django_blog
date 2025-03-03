# Generated by Django 3.2.25 on 2025-02-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='date_created',
            new_name='created_date',
        ),
        migrations.AddField(
            model_name='blog',
            name='counted_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='published_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
