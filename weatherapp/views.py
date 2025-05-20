from django.shortcuts import render
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'Bhadrak')  # Default city
    WEATHER_API_KEY = "aaf83a88258c197ad786f6ebb0f9c1fd"
    UNSPLASH_API_KEY = "NaPXDorEzVqRq2qqO7k-uHGXVXw0Dk2C7WreeaBg4M0"

    # Step 1: Fetch City Details (Including State) Using Geocoding API
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"

    geo_response = requests.get(geo_url).json()
    if not geo_response:
        return render(request, 'weatherapp/home.html', {"error": "Invalid City Name"})

    city_name = geo_response[0]['name']
    state = geo_response[0].get('state', '')  # Some locations may not have a state
    country = geo_response[0]['country']

    # Step 2: Fetch Weather Data
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    weather_response = requests.get(weather_url).json()

    if weather_response.get("cod") != 200:
        return render(request, 'weatherapp/home.html', {"error": "Weather data not found"})

    # Extract weather details
    weather_condition = weather_response['weather'][0]['main'].lower()
    temp = weather_response['main']['temp']
    humidity = weather_response['main']['humidity']
    wind = weather_response['wind']['speed']
    description = weather_response['weather'][0]['description']
    longitude = weather_response['coord']['lon']
    latitude = weather_response['coord']['lat']

    # Step 3: Fetch City Image from Unsplash
    image_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={UNSPLASH_API_KEY}&per_page=1"

    try:
        image_response = requests.get(image_url).json()
        city_image = image_response['results'][0]['urls']['regular'] if image_response['results'] else None
    except Exception as e:
        print(f"Error fetching image: {e}")
        city_image = None

    # Mapping OpenWeatherMap conditions to local static icons
    icon_map = {
        "clear": "clear.png",
        "clouds": "clouds.png",
        "rain": "rain.png",
        "drizzle": "drizzle.png",
        "smoke": "smoke.png",
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
        'city': city_name,
        'state': state,  # ✅ Correct state retrieval
        'country': country,  # ✅ Added country
        'weather': weather_condition.title(),
        'humidity': f"{humidity}%",
        'wind': f"{wind} m/s",
        'longitude': longitude,
        'latitude': latitude,
        'city_image': city_image,
    }
    return render(request, 'weatherapp/home.html', context)