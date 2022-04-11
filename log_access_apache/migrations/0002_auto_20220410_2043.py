# Generated by Django 3.2.12 on 2022-04-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_access_apache', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggingReadFileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Data logging')),
                ('path_file', models.TextField(unique=True, verbose_name='Path file')),
                ('last_line', models.TextField(null=True, verbose_name='Last line')),
                ('last_line_position', models.PositiveBigIntegerField(verbose_name='Last line position')),
            ],
        ),
        migrations.RenameField(
            model_name='logaccessapachemodel',
            old_name='datetime',
            new_name='date',
        ),
    ]