import requests

API_KEY = 'zZXuGdtXZJSh7bZj2NaYFQ56bM29oxzo'
BASE_URL = 'http://dataservice.accuweather.com'

def search_city(city_name):
    try:
        url = f"{BASE_URL}/locations/v1/cities/search"
        params = {
            'apikey': API_KEY,
            'q': city_name,
        }
        request = requests.get(url, params=params)
        if request.status_code == 200:
            data = request.json()
            if data:
                return data[0]['Key'], data[0]['LocalizedName']
            else:
                print("No city found")
        else:
            print(f"Error code: {request.status_code}")
        return None, None
    except Exception as e:
        print(e)

def get_forecast_weather(location_key):
    try:
        url = f"{BASE_URL}/forecasts/v1/daily/5day/{location_key}"
        params = {
            'apikey': API_KEY,
            'metric': 'true'
        }
        request = requests.get(url, params=params)
        if request.status_code == 200:
            return request.json()
        else:
            print(f"Error code: {request.status_code}")
        return None
    except Exception as e:
        print(e)

def get_temperatures(forecast):
    try:
        minimum_temperatures = []
        maximum_temperatures = []
        for day in forecast['DailyForecasts']:
            min_temp = day['Temperature']['Minimum']['Value']
            max_temp = day['Temperature']['Maximum']['Value']
            minimum_temperatures.append(min_temp)
            maximum_temperatures.append(max_temp)
        return (min(minimum_temperatures),
                max(maximum_temperatures),
                sum(minimum_temperatures + maximum_temperatures) / (len(minimum_temperatures) + len(maximum_temperatures)))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    city = input("Write the name of the city to search: ")
    location_key, city_name = search_city(city)
    if location_key:
        forecast = get_forecast_weather(location_key)
        if forecast:
            min_temp, max_temp, avg_temp = get_temperatures(forecast)
            print(f"Forecast for city: {city_name}")
            print(f"Minimum temperatures on the next 5 days: {min_temp}°C")
            print(f"Maximum temperatures on the next 5 days: {max_temp}°C")
            print(f"Average temperatures on the next 5 days: {avg_temp:.2f}°C")
