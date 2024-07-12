# Generated by Django 5.0.6 on 2024-07-12 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='description',
            field=models.TextField(default='Default Discription'),
        ),
        migrations.AddField(
            model_name='upload',
            name='thumbnail',
            field=models.ImageField(default='dictionary.jpg', upload_to='thumbnails/'),
        ),
        migrations.AddField(
            model_name='upload',
            name='video_time',
            field=models.CharField(blank=True, default='00:00', max_length=10),
        ),
    ]
