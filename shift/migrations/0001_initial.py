# Generated by Django 3.2.12 on 2022-03-09 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shift_title', models.CharField(max_length=250)),
                ('shift_start', models.DateTimeField(blank=True, null=True)),
                ('shift_end', models.DateTimeField(blank=True, null=True)),
                ('shift_session', models.CharField(max_length=250)),
                ('shift_short_code', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(1, 'ACTIVE'), (0, 'DEACTIVE')], default=1)),
            ],
            options={
                'db_table': 'shifts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkerShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'ACTIVE'), (2, 'INACTIVE')], db_index=True, default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shift', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shift.shift')),
            ],
            options={
                'db_table': 'worker_shifts',
                'ordering': ['-created_at'],
            },
        ),
    ]
