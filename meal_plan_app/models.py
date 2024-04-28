from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from collections import defaultdict
from multiselectfield import MultiSelectField
from django.utils import timezone


class MealPlan(models.Model):
    title = models.DateField(default = timezone.now)
    meals = models.ManyToManyField('Meals', null=True, blank=True)
    crazy_meals = models.ManyToManyField('Crazy Meals', null=True, blank=True, related_name='crazy_meals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def get_unique_ingredients(self):
        unique_ingredients = defaultdict(float)  # Use defaultdict to automatically initialize ingredient quantities to zero

        for meal in self.meals.all():
            ingredients = meal.ingredients.split(',')  # Assuming ingredients are separated by commas
            for ingredient in ingredients:
                # Extract ingredient name and quantity (if provided)
                parts = ingredient.strip().split(':')
                name = parts[0].strip()
                quantity = float(parts[1].strip()) if len(parts) > 1 else 1.0  # Default quantity is 1.0 if not provided

                # Add ingredient to unique_ingredients dict
                unique_ingredients[name] += quantity

        return dict(unique_ingredients)
    

    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
    

class Meal(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()  # Change this to a JSONField? for structured data
    instructions = models.TextField()
    meal_type = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    



class CrazyMeal(models.Model):
    id_meal = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    instructions = models.TextField()
    source_url = models.URLField()

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    FOOD_PREFRENCES = [
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('pescatarian', 'Pescatarian'),
        ('gluten_free', 'Gluten-Free'),
        ('dairy_free', 'Dairy-Free'),
        ('go_crazy', 'Go Crazy!'),
    ]

    food_preferences = MultiSelectField(choices=FOOD_PREFRENCES,max_length=12, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"Profile for {self.user.username}"
