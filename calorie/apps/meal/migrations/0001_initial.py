# Generated by Django 4.0.4 on 2022-04-27 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='meals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('measure', models.CharField(choices=[('G', 'Gramas'), ('MG', 'Mili Gramas'), ('L', 'Litros'), ('ML', 'Mili Litros')], max_length=2)),
                ('sugar', models.DecimalField(decimal_places=1, max_digits=6)),
                ('fiber', models.DecimalField(decimal_places=1, max_digits=6)),
                ('sodium', models.PositiveIntegerField()),
                ('potassium', models.PositiveIntegerField()),
                ('fat_saturated', models.DecimalField(decimal_places=1, max_digits=6)),
                ('fat_total', models.DecimalField(decimal_places=1, max_digits=6)),
                ('calories', models.PositiveIntegerField()),
                ('cholesterol', models.PositiveIntegerField()),
                ('protein', models.DecimalField(decimal_places=1, max_digits=6)),
                ('carbohydrates_total', models.DecimalField(decimal_places=1, max_digits=6)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='foods', to='meal.meal')),
            ],
        ),
    ]