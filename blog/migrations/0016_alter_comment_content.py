# Generated by Django 4.0 on 2022-01-06 18:02

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_remove_post_slug_alter_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
