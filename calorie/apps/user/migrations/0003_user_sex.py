# Generated by Django 4.0.4 on 2022-04-27 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_max_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMININO')], default='M', max_length=2),
            preserve_default=False,
        ),
    ]
