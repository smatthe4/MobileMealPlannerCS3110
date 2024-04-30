from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile




class MealPlanInfoForm(forms.Form):
    num_meals = forms.IntegerField(label='Number of meals', initial=1, min_value=1, max_value=7)
    category = forms.MultipleChoiceField(
        label='Category',
        choices=[
            ('Vegetarian', 'Vegetarian'),
            ('Vegan', 'Vegan'),
            ('pescatarian', 'Pescatarian'),
            ('gluten_free', 'Gluten-Free'),
            ('dairy_free', 'Dairy-Free')
        ],
        required=False  # Make the field optional
    )
    go_crazy = forms.BooleanField(label='Go Crazy!', required=False)


    widgets = {
        'num_meals': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of meals'}),
        'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        'go_crazy': forms.CheckboxInput(attrs={'class': 'form-control'}),
    }



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=['food_preferences']

        widgest = {
            'food_preferences': forms.CheckboxSelectMultiple(),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }   


        

