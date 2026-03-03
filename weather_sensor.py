import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import io
import logging
import os
from datetime import datetime, timedelta
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"  # 5 day / 3 hour forecast endpoint

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

        # date selection combo: today + next 4 days
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        dates = [(today + timedelta(days=i)).isoformat() for i in range(5)]
        self.date_var = tk.StringVar(value=dates[0])

        ttk.Label(self.master, text="Select City:").pack(pady=5)
        self.city_combo = ttk.Combobox(self.master, textvariable=self.city_var, values=cities)
        self.city_combo.pack(pady=5)
        self.city_combo.bind("<Return>", lambda e: self.check_weather())

        ttk.Label(self.master, text="Select Date:").pack(pady=5)
        self.date_combo = ttk.Combobox(self.master, textvariable=self.date_var, values=dates, state="readonly")
        self.date_combo.pack(pady=5)

        ttk.Checkbutton(self.master, text="Alert if laundry is outside?", variable=self.alert_var).pack(pady=10)
        
        self.check_button = ttk.Button(self.master, text="Check Now", command=self.check_weather)
        self.check_button.pack(pady=5)

        self.icon_label = tk.Label(self.master)
        self.icon_label.pack(pady=10)

        self.status = tk.Label(self.master, text="Ready", wraplength=300, fg="darkblue")
        self.status.pack(pady=10)

        # make window background changeable for visuals
        self.master.config(bg="white")
        self.status.config(bg="white")
        self.icon_label.config(bg="white")

    def periodic_check(self):
        """Thread-safe periodic update using .after()"""
        self.check_weather()
        self.master.after(3600000, self.periodic_check)

    def check_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city.")
            return

        date_str = self.date_var.get()
        self.status.config(text=f"Updating {city} for {date_str}...")

        # dummy mode still uses simple single day data
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

        # decide which endpoint to call
        try:
            if date_str == "" or date_str == datetime.utcnow().date().isoformat():
                params = {"q": city, "appid": API_KEY, "units": "metric"}
                resp = requests.get(BASE_URL, params=params, timeout=5)
                resp.raise_for_status()
                data = resp.json()
            else:
                # forecast lookup
                params = {"q": city, "appid": API_KEY, "units": "metric"}
                resp = requests.get(FORECAST_URL, params=params, timeout=5)
                resp.raise_for_status()
                raw = resp.json()
                data = self.extract_forecast_for_date(raw, date_str)
            if data:
                self.update_ui_with_data(data)
            else:
                raise ValueError("No forecast data available")
        except Exception as e:
            logging.error(f"Network error: {e}")
            self.status.config(text="Error fetching data.", fg="red")

    def extract_forecast_for_date(self, forecast_data, date_str):
        """Return a single data point closest to noon on the requested date."""
        target = datetime.fromisoformat(date_str)
        candidates = []
        for entry in forecast_data.get("list", []):
            dt_txt = entry.get("dt_txt")  # format yyyy-mm-dd hh:mm:ss
            if not dt_txt:
                continue
            try:
                d = datetime.fromisoformat(dt_txt)
            except ValueError:
                continue
            if d.date() == target.date():
                candidates.append((abs((d - datetime.combine(target.date(), datetime.min.time()) - timedelta(hours=12)).total_seconds()), entry))
        if not candidates:
            return None
        # pick the one with smallest distance to midday
        _, best = min(candidates, key=lambda x: x[0])
        return best


    def update_ui_with_data(self, data):
        # Extract data safely with defaults
        weather_main = data.get('weather', [{}])[0].get('main', 'Unknown')
        temp = data.get('main', {}).get('temp', '?')
        humidity = data.get('main', {}).get('humidity', '?')
        icon_code = data.get('weather', [{}])[0].get('icon')
        
        # change background color based on weather
        colors = {
            "Clear": "#87CEEB",
            "Clouds": "#D3D3D3",
            "Rain": "#A9A9A9",
            "Drizzle": "#B0C4DE",
            "Thunderstorm": "#778899",
            "Snow": "#FFFafa",
            "Unknown": "white",
        }
        bg = colors.get(weather_main, "white")
        self.master.config(bg=bg)
        self.status.config(bg=bg)
        self.icon_label.config(bg=bg)

        # Load a nicer, larger icon if available
        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
                icon_res = requests.get(icon_url, stream=True)
                img = Image.open(io.BytesIO(icon_res.content))
                photo = ImageTk.PhotoImage(img)
                self.icon_label.config(image=photo)
                self.icon_label.image = photo
            except Exception:
                pass
        else:
            self.icon_label.config(image="")

        # Format temperature and humidity nicely
        temp_str = f"{temp:.1f}" if isinstance(temp, (int, float)) else temp
        humidity_str = f"{humidity:.0f}" if isinstance(humidity, (int, float)) else humidity
        
        result_text = f"{weather_main}: {temp_str}°C\nHumidity: {humidity_str}%"
        self.status.config(text=result_text, fg="black")

        # Laundry Logic
        if "Rain" in weather_main and self.alert_var.get():
            messagebox.showwarning("Rain Alert", "Bring the laundry in! It's raining.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherSensorApp(root)
    root.mainloop()
