from django.contrib import admin
from .models import Profile, Meal, CrazyMeal, MealPlan

# Register your models here.
admin.site.register(Profile)
admin.site.register(Meal)
admin.site.register(CrazyMeal)
admin.site.register(MealPlan)
