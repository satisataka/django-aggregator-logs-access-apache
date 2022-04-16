# Generated by Django 3.2.12 on 2022-04-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Data logging')),
                ('path_file', models.TextField(db_index=True, unique=True, verbose_name='Path file')),
                ('last_line', models.TextField(blank=True, default='', verbose_name='Last line')),
                ('last_position', models.PositiveBigIntegerField(default=0, verbose_name='Last position')),
            ],
            options={
                'verbose_name': 'File Log',
                'verbose_name_plural': 'File Logs',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='LogAccessApacheModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.GenericIPAddressField(db_index=True, verbose_name='Remote hostname')),
                ('logname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Remote logname')),
                ('user', models.CharField(blank=True, max_length=100, null=True, verbose_name='Remote user')),
                ('date', models.DateTimeField(db_index=True, verbose_name='Request time')),
                ('request_line', models.TextField(blank=True, null=True, verbose_name='First request line')),
                ('status', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Status')),
                ('bytes', models.PositiveIntegerField(blank=True, null=True, verbose_name='Size response in bytes')),
                ('referer', models.TextField(blank=True, null=True, verbose_name='Referer')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='User-Agent')),
            ],
            options={
                'verbose_name': 'Log Access Apache',
                'verbose_name_plural': 'Logs Access Apache',
                'ordering': ['date', 'host'],
            },
        ),
    ]
