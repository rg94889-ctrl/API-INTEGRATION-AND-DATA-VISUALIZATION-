import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates

# Configuration
API_KEY = 'your_api_key_here'  # Replace with your OpenWeatherMap API key
CITY = 'London'  # You can change this to any city
UNITS = 'metric'  # 'metric' for Celsius, 'imperial' for Fahrenheit

# Fetch current weather data
def get_current_weather(api_key, city, units='metric'):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'time': datetime.fromtimestamp(data['dt'])
        }
    else:
        print(f"Error fetching current weather: {data.get('message', 'Unknown error')}")
        return None

# Fetch 5-day forecast data
def get_forecast(api_key, city, units='metric'):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        forecast_data = []
        for item in data['list']:
            forecast_data.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind']['deg'],
                'weather': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
                'pop': item.get('pop', 0)  # Probability of precipitation
            })
        return forecast_data
    else:
        print(f"Error fetching forecast: {data.get('message', 'Unknown error')}")
        return None

# Create visualizations
def create_visualizations(current_data, forecast_data):
    if not current_data or not forecast_data:
        return
    
    # Convert forecast data to DataFrame for easier manipulation
    forecast_df = pd.DataFrame(forecast_data)
    
    # Set style
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))
    
    # Create dashboard with multiple plots
    plt.suptitle(f"Weather Dashboard for {current_data['city']}, {current_data['country']}", fontsize=16, y=1.02)
    
    # Plot 1: Current weather summary
    plt.subplot(2, 2, 1)
    current_metrics = {
        'Temperature (°C)': current_data['temp'],
        'Feels Like (°C)': current_data['feels_like'],
        'Min Temp (°C)': current_data['temp_min'],
        'Max Temp (°C)': current_data['temp_max'],
        'Humidity (%)': current_data['humidity'],
        'Wind Speed (m/s)': current_data['wind_speed']
    }
    sns.barplot(x=list(current_metrics.keys()), y=list(current_metrics.values()), palette="coolwarm")
    plt.title('Current Weather Conditions')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Value')
    
    # Plot 2: Temperature forecast
    plt.subplot(2, 2, 2)
    sns.lineplot(data=forecast_df, x='datetime', y='temp', marker='o', label='Temperature')
    sns.lineplot(data=forecast_df, x='datetime', y='feels_like', marker='o', label='Feels Like')
    plt.title('5-Day Temperature Forecast')
    plt.xlabel('Date/Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.legend()
    
    # Plot 3: Humidity and precipitation probability
    plt.subplot(2, 2, 3)
    ax = sns.lineplot(data=forecast_df, x='datetime', y='humidity', marker='o', color='blue', label='Humidity')
    ax2 = ax.twinx()
    sns.lineplot(data=forecast_df, x='datetime', y='pop', marker='o', color='green', ax=ax2, label='Precipitation Probability')
    plt.title('Humidity and Precipitation Probability')
    plt.xlabel('Date/Time')
    ax.set_ylabel('Humidity (%)', color='blue')
    ax2.set_ylabel('Precipitation Probability', color='green')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    
    # Combine legends from both axes
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper right')
    
    # Plot 4: Wind speed
    plt.subplot(2, 2, 4)
    sns.lineplot(data=forecast_df, x='datetime', y='wind_speed', marker='o', color='purple')
    plt.title('Wind Speed Forecast')
    plt.xlabel('Date/Time')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    
    plt.tight_layout()
    plt.savefig('weather_dashboard.png', bbox_inches='tight', dpi=300)
    plt.show()

# Main execution
if __name__ == "__main__":
    print("Fetching weather data...")
    current_weather = get_current_weather(API_KEY, CITY, UNITS)
    forecast = get_forecast(API_KEY, CITY, UNITS)
    
    if current_weather and forecast:
        print("\nCurrent Weather:")
        print(f"{current_weather['city']}, {current_weather['country']}")
        print(f"Temperature: {current_weather['temp']}°C (Feels like {current_weather['feels_like']}°C)")
        print(f"Weather: {current_weather['weather']} ({current_weather['description']})")
        print(f"Humidity: {current_weather['humidity']}%")
        print(f"Wind: {current_weather['wind_speed']} m/s at {current_weather['wind_deg']}°")
        
        print("\nCreating visualizations...")
        create_visualizations(current_weather, forecast)
        print("Dashboard saved as 'weather_dashboard.png'")
    else:
        print("Failed to fetch weather data. Please check your API key and internet connection.")
