# Generated by Django 4.1 on 2022-08-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_post_options_post_body_post_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='preview',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
