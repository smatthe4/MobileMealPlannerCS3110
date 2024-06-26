# Generated by Django 4.2 on 2024-04-30 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CrazyMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_meal', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('ingredients', models.TextField()),
                ('ingredient_amount', models.TextField(default='')),
                ('instructions', models.TextField()),
                ('source_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ingredients', models.TextField()),
                ('ingredient_amount', models.TextField(null=True)),
                ('instructions', models.TextField()),
                ('food_preferences', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('pescatarian', 'Pescatarian'), ('gluten_free', 'Gluten-Free'), ('dairy_free', 'Dairy-Free')], max_length=55, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_preferences', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('pescatarian', 'Pescatarian'), ('gluten_free', 'Gluten-Free'), ('dairy_free', 'Dairy-Free')], max_length=55, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.DateField(default=django.utils.timezone.now)),
                ('crazy_meal', models.ManyToManyField(to='meal_plan_app.crazymeal')),
                ('meal', models.ManyToManyField(to='meal_plan_app.meal')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meal_plan_app.profile')),
            ],
        ),
    ]
