# Weather Sensor Application

This repository contains a simple **Python** program that simulates a weather sensor with a GUI. It fetches weather data (from OpenWeatherMap or via a dummy generator) and notifies the user when it rains. The user can also tick a checkbox if they have left something outside to dry; when rain is detected and the checkbox is set, an additional alert is shown.

## Features

- Input a city name and retrieve current weather conditions.
- Automatic hourly polling in a background thread.
- Notifications when it starts raining.
- Optional alert for items left outside (checkbox).

## Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Obtain an API key** (optional):
   - Sign up at https://openweathermap.org/api and replace `YOUR_API_KEY_HERE` in `weather_sensor.py` with your key. Without a key the app generates random weather conditions.

3. **Run the app**:

   ```bash
   python weather_sensor.py
   ```

## Usage

- Enter a city name and click **Check Weather**.
- Tick the "Drying items outside?" box to receive a special alert if rain is forecast.
- The app will also poll for updates every hour.

Feel free to extend or customize this application with additional sensors or UI improvements.
