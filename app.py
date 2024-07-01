# Import necessary modules and packages
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import Message
import requests

# Initialize the Flask application
app = Flask(__name__)

# Configure secret key for session management
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'

# Disable SQLALCHEMY_TRACK_MODIFICATIONS to avoid overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Bootstrap5 extension
Bootstrap5(app)

# Initialize SQLAlchemy for database interactions
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# OpenWeatherMap API key
API_KEY = 'f8634d1aa9ff03a6e1e5d747450d6e5d'

# Define custom Jinja filters for formatting timestamps and dates
@app.template_filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%A ')

@app.template_filter('timestamp_to_hour')
def timestamp_to_hour(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')

@app.template_filter('format_date')
def format_date(value, format='%A'):
    date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return date.strftime(format)

# Function to get current weather data for a city
def get_weather(city, unit):
    url = f'https://pro.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        # Fetch UV index data
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        uv_url = f'https://pro.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}'
        uv_response = requests.get(uv_url)
        uv_data = uv_response.json()
        if uv_response.status_code == 200:
            data['uv_index'] = uv_data['value']
        return data
    else:
        return None

# Function to get current weather data by geographic coordinates
def get_weather_by_coords(lat, lon, unit):
    url = f'https://pro.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        uv_url = f'https://pro.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}'
        uv_response = requests.get(uv_url)
        uv_data = uv_response.json()
        if uv_response.status_code == 200:
            data['uv_index'] = uv_data['value']
        return data
    else:
        return None

# Function to get hourly weather forecast for a city
def get_hourly_forecast(city, unit):
    url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&units={unit}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None

# Function to get weekly weather forecast for a city
def get_weekly_forecast(city, unit):
    url = f'https://pro.openweathermap.org/data/2.5/forecast/climate?q={city}&units={unit}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None

# Function to determine weather class based on weather code
def determine_weather_class(weather_code):
    if weather_code // 100 == 2:
        return 'thunderstorm'
    elif weather_code // 100 == 3:
        return 'drizzle'
    elif weather_code // 100 == 5:
        return 'rainy'
    elif weather_code // 100 == 6:
        return 'snowy'
    elif weather_code // 100 == 7:
        return 'misty'
    elif weather_code == 800:
        return 'sunny'
    elif weather_code // 100 == 8:
        return 'cloudy'
    else:
        return ''

# Mapping of weather icon codes to image filenames
WEATHER_ICON_MAP = {
    '01d': 'clear_sky_day.png',
    '01n': 'clear_sky_night.png',
    '02d': 'few_clouds_day.png',
    '02n': 'few_clouds_night.png',
    '03d': 'scattered_clouds_day.png',
    '03n': 'scattered_clouds_night.png',
    '04d': 'broken_clouds_day.png',
    '04n': 'broken_clouds_night.png',
    '09d': 'shower_rain_day.png',
    '09n': 'shower_rain_night.png',
    '10d': 'rain_day.png',
    '10n': 'rain_night.png',
    '11d': 'thunderstorm_day.png',
    '11n': 'thunderstorm_night.png',
    '13d': 'snow_day.png',
    '13n': 'snow_night.png',
    '50d': 'mist_day.png',
    '50n': 'mist_night.png'
}

# Mapping of detailed weather descriptions to simpler descriptions
SIMPLE_DESCRIPTION_MAP = {
    "thunderstorm with light rain": "Light Thunderstorm",
    "thunderstorm with rain": "Thunderstorm",
    "thunderstorm with heavy rain": "Heavy Thunderstorm",
    "light thunderstorm": "Light Thunderstorm",
    "thunderstorm": "Thunderstorm",
    "heavy thunderstorm": "Heavy Thunderstorm",
    "ragged thunderstorm": "Thunderstorm",
    "thunderstorm with light drizzle": "Light Thunderstorm",
    "thunderstorm with drizzle": "Thunderstorm",
    "thunderstorm with heavy drizzle": "Heavy Thunderstorm",
    "light intensity drizzle": "Light Drizzle",
    "drizzle": "Drizzle",
    "heavy intensity drizzle": "Heavy Drizzle",
    "light intensity drizzle rain": "Light Rain",
    "drizzle rain": "Rain",
    "heavy intensity drizzle rain": "Heavy Rain",
    "shower rain and drizzle": "Rain",
    "heavy shower rain and drizzle": "Heavy Rain",
    "shower drizzle": "Drizzle",
    "light rain": "Light Rain",
    "moderate rain": "Rain",
    "heavy intensity rain": "Heavy Rain",
    "very heavy rain": "Very Heavy Rain",
    "extreme rain": "Extreme Rain",
    "freezing rain": "Freezing Rain",
    "light intensity shower rain": "Light Rain",
    "shower rain": "Rain",
    "heavy intensity shower rain": "Heavy Rain",
    "ragged shower rain": "Rain",
    "light snow": "Light Snow",
    "snow": "Snow",
    "heavy snow": "Heavy Snow",
    "sleet": "Sleet",
    "light shower sleet": "Light Sleet",
    "shower sleet": "Sleet",
    "light rain and snow": "Rain And Snow",
    "rain and snow": "Rain And Snow",
    "light shower snow": "Light Snow",
    "shower snow": "Snow",
    "heavy shower snow": "Heavy Snow",
    "mist": "Mist",
    "smoke": "Smoke",
    "haze": "Haze",
    "sand/ dust whirls": "Dust",
    "fog": "Fog",
    "sand": "Sand",
    "dust": "Dust",
    "volcanic ash": "Volcanic Ash",
    "squalls": "Squalls",
    "tornado": "Tornado",
    "clear sky": "Clear",
    "few clouds": "Few Clouds",
    "scattered clouds": "Scattered Clouds",
    "broken clouds": "Broken Clouds",
    "overcast clouds": "Overcast Clouds"
}

# Define route for the home page
@app.route('/', methods=['GET'])
def index():
    city = request.args.get('city', 'Berlin')
    unit = request.args.get('unit', 'metric')
    weather_data = get_weather(city, unit)
    hourly_forecast_data = get_hourly_forecast(city, unit)
    weekly_forecast_data = get_weekly_forecast(city, unit)

    if weather_data and 'weather' in weather_data:
        weather_code = weather_data['weather'][0]['id']
        icon_code = weather_data['weather'][0]['icon']
        weather_icon = WEATHER_ICON_MAP.get(icon_code, 'default.png')
        weather_class = determine_weather_class(weather_code)
        description = weather_data['weather'][0]['description']
        simple_description = SIMPLE_DESCRIPTION_MAP.get(description, description)
        return render_template('index.html', weather_data=weather_data, hourly_forecast_data=hourly_forecast_data, weekly_forecast_data=weekly_forecast_data, unit=unit,
                               weather_class=weather_class, city=city, weather_icon=weather_icon, simple_description=simple_description,
                               WEATHER_ICON_MAP=WEATHER_ICON_MAP, SIMPLE_DESCRIPTION_MAP=SIMPLE_DESCRIPTION_MAP)
    else:
        error_message = "City not found. Please try another city."
        return render_template('index.html', error_message=error_message, city=city, unit=unit)

# Define route for getting weather data based on geographic coordinates
@app.route('/geo_weather', methods=['GET'])
def geo_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    unit = request.args.get('unit', 'metric')
    weather_data = get_weather_by_coords(lat, lon, unit)
    city = weather_data['name'] if weather_data else 'Unknown'
    hourly_forecast_data = get_hourly_forecast(city, unit)
    weekly_forecast_data = get_weekly_forecast(city, unit)

    if weather_data and 'weather' in weather_data:
        weather_code = weather_data['weather'][0]['id']
        icon_code = weather_data['weather'][0]['icon']
        weather_icon = WEATHER_ICON_MAP.get(icon_code, 'default.png')
        weather_class = determine_weather_class(weather_code)
        description = weather_data['weather'][0]['description']
        simple_description = SIMPLE_DESCRIPTION_MAP.get(description, description)
        return render_template('index.html', weather_data=weather_data, hourly_forecast_data=hourly_forecast_data, weekly_forecast_data=weekly_forecast_data, unit=unit,
                               weather_class=weather_class, city=city, weather_icon=weather_icon, simple_description=simple_description,
                               WEATHER_ICON_MAP=WEATHER_ICON_MAP, SIMPLE_DESCRIPTION_MAP=SIMPLE_DESCRIPTION_MAP)
    else:
        error_message = "Location not found. Please try again."
        return render_template('index.html', error_message=error_message, city=city, unit=unit)

# Define route for the "About" page
@app.route('/about')
def about():
    return render_template('about.html')

# Define route for the "Contact" page with GET and POST methods
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first-name', '').strip()
            last_name = request.form.get('last-name', '').strip()
            email = request.form.get('email', '').strip()
            phone_number = request.form.get('phone-number', '').strip()
            subject = request.form.get('subject', '').strip()
            message_content = request.form.get('message', '').strip()

            # Check if required fields are filled
            if not (first_name and last_name and email and subject and message_content):
                raise ValueError("All fields except phone number are required.")

            # Create a new message instance
            new_message = Message(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                subject=subject,
                message=message_content
            )

            # Add and commit the new message to the database
            db.session.add(new_message)
            db.session.commit()

            return redirect(url_for('success'))

        except (BadRequestKeyError, ValueError) as e:  # type: ignore
            return render_template('contact.html', error=str(e))

    return render_template('contact.html')

# Define route for the success page
@app.route('/success')
def success():
    return render_template('success.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
