# Generated by Django 4.0 on 2022-01-04 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_rename_body_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.TextField(default='Unknown', max_length=32),
        ),
    ]
