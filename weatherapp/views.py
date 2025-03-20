from django.shortcuts import render, HttpResponse
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    city = request.POST.get('city', 'Indore')  # Default city
    API_KEY = "aaf83a88258c197ad786f6ebb0f9c1fd"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    PARAMS = {'units': 'metric'}

    response = requests.get(url, params=PARAMS).json()

    if response.get("cod") != 200:  # Invalid city handling
        return render(request, 'weatherapp/home.html', {"error": "Invalid City Name"})

    # Extract weather details
    weather_condition = response['weather'][0]['main'].lower()
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    wind = response['wind']['speed']
    description = response['weather'][0]['description']

    # Mapping OpenWeatherMap conditions to local static icons
    icon_map = {
        "clear": "clear.png",
        "clouds": "clouds.png",
        "rain": "rain.png",
        "drizzle": "drizzle.png",
        "thunderstorm": "thunderstorm.png",
        "snow": "snow.png",
        "mist": "mist.png",
        "haze": "haze.png",
        "fog": "fog.png",
        "sand": "dust.png",
        "dust": "dust.png",
    }

    icon_filename = icon_map.get(weather_condition, "default.png")

    # Prepare context data
    context = {
        'description': description.title(),
        'temp': f"{temp}°C",
        'icon': icon_filename,
        'day': datetime.datetime.today().strftime('%A, %d %B %Y'),
        'city': city.capitalize(),
        'weather': weather_condition.title(),
        'humidity': f"{humidity}%",
        'wind': f"{wind} m/s"
    }

    return render(request, 'weatherapp/home.html', context)
    