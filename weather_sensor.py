import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import io
import logging
import os

# API key placeholder. When left as "YOUR_API_KEY_HERE" the app
# runs in dummy mode and does not make real network requests.
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherSensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather Sensor Pro")
        master.geometry("350x450")

        # UI Setup
        self.setup_ui()
        
        # Schedule the first periodic check (3600000 ms = 1 hour)
        self.master.after(3600000, self.periodic_check)

    def setup_ui(self):
        cities = ["London", "New York", "Paris", "Tokyo", "Sydney", "Mumbai"]
        self.city_var = tk.StringVar(value=cities[0])
        self.alert_var = tk.BooleanVar()

        ttk.Label(self.master, text="Select City:").pack(pady=5)
        self.city_combo = ttk.Combobox(self.master, textvariable=self.city_var, values=cities)
        self.city_combo.pack(pady=5)
        self.city_combo.bind("<Return>", lambda e: self.check_weather())

        ttk.Checkbutton(self.master, text="Alert if laundry is outside?", variable=self.alert_var).pack(pady=10)
        
        self.check_button = ttk.Button(self.master, text="Check Now", command=self.check_weather)
        self.check_button.pack(pady=5)

        self.icon_label = tk.Label(self.master)
        self.icon_label.pack(pady=10)

        self.status = tk.Label(self.master, text="Ready", wraplength=300, fg="darkblue")
        self.status.pack(pady=10)

    def periodic_check(self):
        """Thread-safe periodic update using .after()"""
        self.check_weather()
        self.master.after(3600000, self.periodic_check)

    def check_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city.")
            return

        self.status.config(text=f"Updating {city}...")
        
        # If running in dummy mode generate fake data instead of calling the API
        if API_KEY == "YOUR_API_KEY_HERE":
            import random
            cond = random.choice(["Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm"])
            temp_c = random.uniform(-10, 35)
            humidity = random.uniform(30, 90)
            dummy = {
                "weather": [{"main": cond, "description": cond.lower(), "icon": "01d"}],
                "main": {"temp": temp_c, "humidity": humidity},
            }
            logging.info(f"Dummy weather: {cond} {temp_c:.1f}C")
            self.update_ui_with_data(dummy)
            return

        try:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            # Reference: OpenWeatherMap Current Weather API (https://openweathermap.org)
            resp = requests.get(BASE_URL, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            self.update_ui_with_data(data)
        except Exception as e:
            logging.error(f"Network error: {e}")
            self.status.config(text="Error fetching data.", fg="red")

    def update_ui_with_data(self, data):
        # Extract data safely with defaults
        weather_main = data.get('weather', [{}])[0].get('main', 'Unknown')
        temp = data.get('main', {}).get('temp', '?')
        humidity = data.get('main', {}).get('humidity', '?')
        icon_code = data.get('weather', [{}])[0].get('icon')
        
        # Load Icon if one exists
        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_res = requests.get(icon_url, stream=True)
                img = Image.open(io.BytesIO(icon_res.content))
                photo = ImageTk.PhotoImage(img)
                self.icon_label.config(image=photo)
                self.icon_label.image = photo
            except Exception:
                pass
        else:
            self.icon_label.config(image="")

        result_text = f"{weather_main}: {temp}°C\nHumidity: {humidity}%"
        self.status.config(text=result_text, fg="black")

        # Laundry Logic
        if "Rain" in weather_main and self.alert_var.get():
            messagebox.showwarning("Rain Alert", "Bring the laundry in! It's raining.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherSensorApp(root)
    root.mainloop()
