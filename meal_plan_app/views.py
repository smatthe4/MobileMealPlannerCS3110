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




# Create your views here.
def index(request):
    form = MealPlanInfoForm()
    return render(request, 'meal_plan_app/index.html', {'form': form})

def logoutView(request):
    logout(request)
    return render(request, 'registration/logout_complete.html')


def meal_list(request):
    if request.method == 'POST':
        form = MealPlanInfoForm(request.POST)
    
        if form.is_valid():
            go_crazy = form.cleaned_data['go_crazy']
            num_meals = form.cleaned_data['num_meals']
            category = form.cleaned_data['category']

            
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
                            # Create CrazyMeal instance
                            crazy_meal = CrazyMeal.objects.create(
                                id_meal=meal_data['idMeal'],
                                name=meal_data['strMeal'],
                                category=meal_data['strCategory'],
                                instructions=meal_data['strInstructions'],
                                source_url=meal_data['strSource']
                            )
                            crazy_meals.append(crazy_meal)
                        else:
                            # Return error response if request was not successful
                            return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
                    except Exception as e:
                        # Return error response if an exception occurs
                        return JsonResponse({'error': str(e)}, status=500)
                
                # Create a meal plan instance
                meal_plan = MealPlan.objects.create()
                meal_plan.crazy_meal.add(*crazy_meals)
                
            else:
                # Retrieve meals from the database based on the selected category
                meals = Meal.objects.filter(food_preferences=category)
                selected_meals = random.sample(list(meals), min(num_meals, len(meals)))
                
                # Create a meal plan instance
                meal_plan = MealPlan.objects.create()
                meal_plan.meal.add(*selected_meals)


        # Optionally, associate the meal plan with the current user
        if request.user.is_authenticated:
            meal_plan.user = request.user
            meal_plan.save()
        # Render the generated meal plan
        return render(request, 'meal_plan_app/meal_list.html', {'meal_plan': meal_plan})

    else:
        form = MealPlanInfoForm()
    return render(request, 'meal_plan_app/index.html', {'form': form})



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



