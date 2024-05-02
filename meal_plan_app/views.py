from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
import requests, random
from django.contrib.auth.models import Group
from .decorators import allowed_users, user_is_owner
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.views import generic
from django.shortcuts import redirect



# Create your views here.
def index(request):
    form = MealPlanInfoForm()
    return render(request, 'meal_plan_app/index.html', {'form': form})

def logoutView(request):
    logout(request)
    return render(request, 'registration/logout_complete.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['regular_user'])
def save_to_profile(request):
    if request.method == 'POST':
        meal_plan_id = request.POST.get('meal_plan_id')
        if meal_plan_id:
            try:
                meal_plan = MealPlan.objects.get(id=meal_plan_id)
                # Assuming the user is authenticated, you can access the user through request.user
                user_profile = Profile.objects.get(user=request.user)
                user_profile.meal_plan = meal_plan
                user_profile.save()
                messages.success(request, 'Meal plan saved to your profile successfully.')
            except MealPlan.DoesNotExist:
                messages.error(request, 'Meal plan not found.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found.')
        else:
            messages.error(request, 'Invalid request.')
    return redirect('meal_list')


def meal_list(request):
    if request.method == 'POST':
        form = MealPlanInfoForm(request.POST)
        if form.is_valid():
            go_crazy = form.cleaned_data['go_crazy']
            num_meals = form.cleaned_data['num_meals']
            category = form.cleaned_data['category']

            # Create a meal plan instance
            meal_plan = MealPlan.objects.create()

            if go_crazy:
                crazy_meals = []
                for _ in range(num_meals):
                    try:
                        # Make GET request to the API endpoint
                        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
                        # Check if request was successful (status code 200)
                        if response.status_code == 200:
                            # Parse JSON response
                            data = response.json()
                            # Extract meal data
                            meal_data = data['meals'][0]  # Assuming the response contains meal data
                            # Check if the meal already exists in the database
                            if CrazyMeal.objects.filter(id_meal=meal_data['idMeal']).exists():
                                crazy_meal = CrazyMeal.objects.get(id_meal=meal_data['idMeal'])
                            else:
                                # Create CrazyMeal instance
                                crazy_meal = CrazyMeal.objects.create(
                                    id_meal=meal_data['idMeal'],
                                    name=meal_data['strMeal'],
                                    category=meal_data['strCategory'],
                                    instructions=meal_data['strInstructions'],
                                    source_url=meal_data['strSource'],
                                    ingredients=', '.join([meal_data[f'strIngredient{i}'] for i in range(1, 21) if meal_data.get(f'strIngredient{i}')]),
                                    ingredient_amount=', '.join([meal_data[f'strMeasure{i}'] for i in range(1, 21) if meal_data.get(f'strMeasure{i}')]),
                                )
                            crazy_meals.append(crazy_meal)
                    except Exception as e:
                        # Handle exceptions, such as API errors
                        print(f"Error creating CrazyMeal: {e}")

                # Add crazy meals to the meal plan
                meal_plan.crazy_meal.add(*crazy_meals)
            if not go_crazy:
                # Retrieve meals from the database based on the selected category
                meals = Meal.objects.all()
                selected_meals = random.sample(list(meals), min(num_meals, len(meals)))
                # Add selected meals to the meal plan
                meal_plan.meal.add(*selected_meals)

            # Render the generated meal plan
            return render(request, 'meal_plan_app/meal_list.html', {'meal_plan': meal_plan})

    else:
        form = MealPlanInfoForm()
    return render(request, 'meal_plan_app/index.html', {'form': form})


def groceryList(request, meal_plan_id):
    # Retrieve the MealPlan instance
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id)

    # Call the get_unique_ingredients() method to get the unique ingredients
    unique_ingredients = meal_plan.get_unique_ingredients()

    # Convert the dictionary of unique ingredients into a list of tuples
    unique_ingredients_list = list(unique_ingredients.items())

    # Render the grocery list template and pass the unique ingredients list
    return render(request, 'meal_plan_app/grocery_list.html', {'unique_ingredients_list': unique_ingredients_list})


def logoutView(request):
    logout(request)
    return render(request, 'registration/logout_complete.html')


def registerPage(request):
   form = CreateUserForm()

   if request.method =='POST':
      form = CreateUserForm(request.POST)
      if form.is_valid():
         user = form.save()
         username = form.cleaned_data.get('username')
         group = Group.objects.get(name='regular_user')
         user.groups.add(group)
         userprofile = Profile.objects.create(user=user,)
         userprofile.save()

         messages.success(request, 'Account was created for ' + username)
         return redirect('login')
      
   context = {'form': form}
   return render(request, 'registration/register.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['regular_user'])
@user_is_owner()
def updateProfile(request, profile_id):
   profile = get_object_or_404(Profile, pk=profile_id)
   
   if request.method == 'POST':
      #Create a new dictionary with form data and group_id
      profile_data = request.POST.copy()
      profile_data['profile_id'] = profile_id
      form = ProfileForm(request.POST, instance=profile)
      if form.is_valid():
         #Save the form without committing to the database
         profile = form.save(commit=False)
         #Set the group relationship
         profile.profile = profile
         profile.save()

         #redirect back to the group detail page
         return redirect('user_page')
   else:
      form = ProfileForm(instance=profile)

   context = {'form': form, 'profile': profile}
   return render(request, 'meal_plan_app/update_profile.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['regular_user'])
@user_is_owner()
def userPage(request):
   userProfile = request.user.profile
   form = ProfileForm(instance = userProfile)
   print('organization', userProfile)
   if request.method == 'POST':
      form = ProfileForm(request.POST, request.FILES, instance=userProfile)
      if form.is_vaild():
         form.save()
   context = {'userProfile': userProfile, 'form':form}
   return render(request, 'meal_plan_app/user.html', context)


def recipe(request, pk):
    meal = Meal.objects.get(pk=pk)

    ingredients = [ingredient.strip() for ingredient in meal.ingredients.split(',')]
    amounts = [amount.strip() for amount in meal.ingredient_amount.split(',')]
    ingredient_list = list(zip(ingredients, amounts))
    

    instructions = meal.instructions.split('.')


    context = {'meal': meal, 'ingredient_list': ingredient_list, 'instructions': instructions}
    return render(request, 'meal_plan_app/recipe.html', context)

def crazyRecipe(request, pk):
    crazymeal = CrazyMeal.objects.get(pk=pk)

    ingredients = [ingredient.strip() for ingredient in crazymeal.ingredients.split(',')]
    amounts = [amount.strip() for amount in crazymeal.ingredient_amount.split(',')]
    ingredient_list = list(zip(ingredients, amounts))
    

    instructions = crazymeal.instructions.split('.')


    context = {'crazy_meal': crazymeal, 'ingredient_list': ingredient_list, 'instructions': instructions}
    return render(request, 'meal_plan_app/crazy_recipe.html', context)





