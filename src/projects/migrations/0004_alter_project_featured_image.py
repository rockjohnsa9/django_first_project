# Generated by Django 3.2.4 on 2022-02-28 03:05

from django.db import migrations, models
import helpers.upload_file_name


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=helpers.upload_file_name.content_file_name),
        ),
    ]