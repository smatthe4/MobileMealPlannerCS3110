from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'meal_plan_app/index.html')

def mealist(request):
    return render(request, 'meal_plan_app/mealistwip.html')