# Generated by Django 5.1.2 on 2024-10-29 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='rating',
            field=models.FloatField(default=0.0, verbose_name='Đánh giá'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Tiêu đề'),
        ),
    ]