# Generated by Django 4.0 on 2022-01-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default='Unknown', max_length=32),
        ),
    ]
