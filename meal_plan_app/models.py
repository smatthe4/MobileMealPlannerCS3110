from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from collections import defaultdict

"""
class MealPlan(models.Model):
    title = models.CharField(max_length=100)
    meals = models.ManyToManyField('Meal')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')


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
    ingredients = models.TextField()  # You might want to change this to a JSONField if you need more structured data
    instructions = models.TextField()
    api_id = models.CharField(max_length=100)  # Assuming this is an ID from the external API

    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"Profile for {self.user.username}"
"""