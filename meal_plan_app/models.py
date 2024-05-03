from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from collections import defaultdict
from multiselectfield import MultiSelectField
from django.utils import timezone



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
        return reverse("meal_detail", args=[str(self.id)])
    
    def __str__(self):
        return self.title
    



class CrazyMeal(models.Model):
    id_meal = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    ingredients = models.TextField()
    ingredient_amount = models.TextField(default='')
    instructions = models.TextField()
    source_url = models.URLField()



    def get_absolute_url(self):
        return reverse("cmeal_detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    title = models.DateField(default = timezone.now)
    meal = models.ManyToManyField('Meal')
    crazy_meal = models.ManyToManyField('CrazyMeal')
    

    def get_unique_ingredients(self):
        unique_ingredients = {}
        
        # Loop through meals and add ingredients
        for meal in self.meal.all():
            for ingredient_line, amount_line in zip(meal.ingredients.split(','), meal.ingredient_amount.split(',')):
                name = ingredient_line.strip()  # Assuming each line contains only the ingredient name
                amount = amount_line.strip()    # Assuming each line contains only the ingredient amount
                ingredient_obj = {'name': name, 'amount': amount}
                if ingredient_obj['name'] in unique_ingredients:
                    unique_ingredients[ingredient_obj['name']] += ingredient_obj['amount']
                else:
                    unique_ingredients[ingredient_obj['name']] = ingredient_obj['amount']

        # Loop through crazy meals and add ingredients
        for crazy_meal in self.crazy_meal.all():
            for ingredient_line, amount_line in zip(crazy_meal.ingredients.split(','), crazy_meal.ingredient_amount.split(',')):
                name = ingredient_line.strip()  # Assuming each line contains only the ingredient name
                amount = amount_line.strip()    # Assuming each line contains only the ingredient amount
                ingredient_obj = {'name': name, 'amount': amount}
                if ingredient_obj['name'] in unique_ingredients:
                    unique_ingredients[ingredient_obj['name']] += ingredient_obj['amount']
                else:
                    unique_ingredients[ingredient_obj['name']] = ingredient_obj['amount']
        
        return unique_ingredients



    def get_absolute_url(self):
        return reverse("meal_plan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
   


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
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.user.username
    

 