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
import requests




# Create your views here.
def index(request):
    return render(request, 'meal_plan_app/index.html')

def mealist(request):
    if request.method == 'POST':
        # Get user input from the form
        num_meals = int(request.POST.get('num_meals', 1))  # Default to 1 if not specified
        category = request.POST.get('category')

        # URL of the MealDB API endpoint to fetch random meals by category
        api_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'

        try:
            # Make a GET request to the API
            response = requests.get(api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()
                # Extract random meals from the response data
                random_meals = data['meals'][:num_meals]  # Limit to the specified number of meals
                # Create a new MealPlan object
                meal_plan = MealPlan.objects.create(title=f"{num_meals} Random Meals - {category}")
                # Iterate over the random meals and save them to the MealPlan
                for meal_data in random_meals:
                    # Create a new Meal object and fill its fields with the retrieved data
                    meal = Meal.objects.create(
                        id_meal=meal_data['idMeal'],
                        name=meal_data['strMeal'],
                        category=category,  # Use the specified category
                        # Other fields...
                    )
                    # Add the meal to the MealPlan
                    meal_plan.meals.add(meal)
                # Return success response
    return render(request, 'meal_plan_app/mealistwip.html')


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
        # group = UserProfile.objects.get(name='organization_role')
         #user.groups.add(group)
         organization = UserProfile.objects.create(user=user,)
         organization.save()

         messages.success(request, 'Account was created for ' + username)
         return redirect('login')
      
   context = {'form': form}
   return render(request, 'registration/register.html', context)

 


@login_required(login_url='login')
#@allowed_users(allowed_roles=['organization_role'])
#@user_is_owner()
def userPage(request):
   organization = request.user.organization
   form = UserProfileForm(instance = organization)
   print('userProfile', UserProfile)
   if request.method == 'POST':
      form = UserProfileForm(request.POST, request.FILES, instance=organization)
      if form.is_vaild():
         form.save()
   context = {'organization': organization, 'form':form}
   return render(request, 'parent_resource_app/user.html', context)




def get_random_meal(request):
        # API endpoint URL
        api_url = 'https://www.themealdb.com/api/json/v1/1/random.php'

        try:
            # Make GET request to the API endpoint
            response = requests.get(api_url)
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()
                # Extract meal data
                meal = data['meals'][0]  # Assuming the response contains meal data
                # Return JSON response with meal data
                return JsonResponse({'meal': meal})
            else:
                # Return error response if request was not successful
                return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
        except Exception as e:
            # Return error response if an exception occurs
            return JsonResponse({'error': str(e)}, status=500)
