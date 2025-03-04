import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = '69001fdf7b09f3cd686f02ecfb01fcf4'
CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?'


@app.route('/', methods=['GET', 'POST'])
# User first visits the page - GET request
#User submits the form (entering city name) - POST request
def index():
# route to handle the home page. Route will render HTML form where user can input city name

    weather_data = None
    forecast_list = None
    error_message = None

    if request.method == 'POST':
        city = request.form['city'] # Get city from form

        if city: # if there is input, API call to openweather
            # Fetch Current Weather
            weather_url = CURRENT_WEATHER_URL + 'q=' + city + '&appid=' + API_KEY + '&units=metric'
            weather_response = requests.get(weather_url) # send request to openweather
            weather_data = weather_response.json()  # Parse the JSON response

            # Fetch 5-day forecast
            forecast_url = FORECAST_URL + 'q=' + city + '&appid=' + API_KEY + '&units=metric'
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if weather_data['cod'] == 200:  # Check if the response is valid (status 200 means success)
                # Parse the relevant weather data
                main_data = weather_data['main']
                weather_info = weather_data['weather'][0]
                weather_data = {
                    'city': city,
                    'temperature': main_data['temp'],
                    'pressure': main_data['pressure'],
                    'humidity': main_data['humidity'],
                    'description': weather_info['description'],
                    'icon': weather_info['icon'],
                }
            else:
                weather_data = None
                error_message = "City not found. Please try again."

            forecast_list = []
            if forecast_data.get('cod') == "200":
                for item in forecast_data['list']:
                    time = item['dt_txt'].split(' ')[1]
                    if time == "12:00:00": # Get noon data for each day.
                        forecast_list.append({
                            'date': item['dt_txt'].split(' ')[0],
                            'temperature': item['main']['temp'],
                            'description': item['weather'][0]['description'],
                            'icon': item['weather'][0]['icon'],
                        })

    return render_template('index.html', weather_data=weather_data, forecast_list=forecast_list, error_message=error_message)

if __name__ == '__main__':
            app.run(debug=True)