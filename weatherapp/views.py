from django.shortcuts import render, HttpResponse
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=aaf83a88258c197ad786f6ebb0f9c1fd'
    PARAMS = {'units':'metric'}

    data = requests.get(url, params=PARAMS).json()
    weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = data['main']['temp']
    icon = data['weather'][0]['icon']
    day = datetime.datetime.today()
    return render(request, 'weatherapp/home.html',{'description':description,
                                                       'temp':temp,
                                                       'icon':icon,
                                                       'day':day,
                                                       'city':city,
                                                       'weather':weather})