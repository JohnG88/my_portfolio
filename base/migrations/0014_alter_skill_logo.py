# Generated by Django 4.0.3 on 2022-04-10 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_skill_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='logo',
            field=models.ImageField(default='gear.png', null=True, upload_to=''),
        ),
    ]