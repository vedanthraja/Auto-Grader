# Generated by Django 3.1.7 on 2021-02-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210227_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='image',
            field=models.ImageField(upload_to='myapp/uploads/'),
        ),
    ]
