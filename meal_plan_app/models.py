from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from collections import defaultdict
from multiselectfield import MultiSelectField
from django.utils import timezone





class Profile(models.Model):
    FOOD_PREFRENCES = [
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('pescatarian', 'Pescatarian'),
        ('gluten_free', 'Gluten-Free'),
        ('dairy_free', 'Dairy-Free'),
    ]

    food_preferences = MultiSelectField(choices=FOOD_PREFRENCES, max_length=55, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)     


    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.user.username
    

 

class Meal(models.Model):


    FOOD_PREFRENCES = [
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('pescatarian', 'Pescatarian'),
        ('gluten_free', 'Gluten-Free'),
        ('dairy_free', 'Dairy-Free'),
    ]
    title = models.CharField(max_length=100)
    ingredients = models.TextField()  
    ingredient_amount = models.TextField(null=True)
    instructions = models.TextField()
    food_preferences = MultiSelectField(choices=FOOD_PREFRENCES,max_length=55, null=True, blank=True)


    def get_absolute_url(self):
        return reverse("meal_plan_detail", args=[str(self.id)])
    
    def __str__(self):
        return self.title
    



class CrazyMeal(models.Model):
    id_meal = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    ingredients = models.TextField()
    ingredient_amount = models.TextField()
    instructions = models.TextField()
    source_url = models.URLField()

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    title = models.DateField(default = timezone.now)
    meal = models.ManyToManyField('Meal')
    crazy_meal = models.ManyToManyField('CrazyMeal')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)


    def get_unique_ingredients(self):
        unique_ingredients = {}
        
        # Loop through meals and add ingredients
        for meal in self.meal.all():
            for ingredient in meal.ingredient_set.all():
                if ingredient.name in unique_ingredients:
                    unique_ingredients[ingredient.name] += ingredient.amount
                else:
                    unique_ingredients[ingredient.name] = ingredient.amount
        
        # Loop through crazy meals and add ingredients
        for crazy_meal in self.crazy_meal.all():
            for ingredient in crazy_meal.ingredient:
                if ingredient.name in unique_ingredients:
                    unique_ingredients[ingredient.name] += ingredient.amount
                else:
                    unique_ingredients[ingredient.name] = ingredient.amount
        
        # Format ingredients into tuple
        ingredients_tuple = tuple(f"{name}: {amount}" for name, amount in unique_ingredients.items())
        
        return ingredients_tuple




    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
   

