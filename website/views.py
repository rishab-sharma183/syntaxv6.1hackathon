from flask import Blueprint, request, render_template, redirect, url_for
import geocoder
import requests
from .staticdata import cities
import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=["GET"])
def redir():
    return redirect(url_for('views.weather'))


@views.route('/weather', methods=["GET", "POST"])
def weather():
    ip = request.remote_addr
    geo_location = geocoder.ip(ip)
    print(request.remote_addr)
    city = geo_location.city
    if request.args.get('city'):
        city = request.args.get('city')
    print(geo_location.latlng, geo_location.city)
    if request.method == "POST":
        city = request.form.get('city')

    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    url2 = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city, "days": "3"}
    querystring2 = {"q": city}

    headers = {
        "X-RapidAPI-Key": "e7c36d5797mshd71062d4e8e481fp14e867jsn504cabd7da67",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    response2 = requests.request("GET", url2, headers=headers, params=querystring2).json()

    if response.get('error', None):
        return response['error']['message']
    else:
        weather_main = response2['current']['condition']['text']
        temperature = response2['current']['temp_c']
        is_day = response2['current']['is_day']
        wind_speed = response2['current']['wind_kph']
        wind_dir = response2['current']['wind_dir']
        humidity = response2['current']['humidity']
        icon_link = response2['current']['condition']['icon']
        actual_location = response2['location']['name'] + ", " + response2['location']['region']
        future_forecasts = []
        for forecast in response['forecast']['forecastday']:
            date_ls = list(map(int, forecast['date'].split('-')))
            date = datetime.date(date_ls[0], date_ls[1], date_ls[2])
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            future_forecasts.append({"weather":forecast['day']['condition']['text'], "icon":forecast['day']['condition']['icon'], "temp":forecast['day']['avgtemp_c'], "day":days[date.weekday()],  "date":forecast['date']})

        print(future_forecasts)
        return render_template('home.html',
                           data={'city': city, 'weather': weather_main, 'temp': temperature, 'wind_speed': wind_speed, "wind_dir": wind_dir, "humidity": humidity, "icon_src":icon_link, "loc":actual_location}, cities=cities['data'], future=future_forecasts)
