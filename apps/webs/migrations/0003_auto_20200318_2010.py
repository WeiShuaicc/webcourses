# Generated by Django 2.2 on 2020-03-18 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webs', '0002_auto_20200318_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='id',
        ),
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='姓名'),
        ),
    ]
