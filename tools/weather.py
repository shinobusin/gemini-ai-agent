import json
import urllib.parse
import urllib.request

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather(city: str) -> str:
    """Returns live weather conditions plus a 3-day daily min/max temperature and rain probability forecast for a city."""
    try:
        encoded_city = urllib.parse.quote(city)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1"
        with urllib.request.urlopen(geo_url, timeout=10) as res:
            geo_data = json.loads(res.read().decode())

        if not geo_data.get("results"):
            return f"Could not find coordinates for city: {city}"

        place = geo_data["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        resolved_name = f"{place['name']}, {place.get('country', '')}"

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&timezone=auto&forecast_days=3"
        )
        with urllib.request.urlopen(weather_url, timeout=10) as res:
            data = json.loads(res.read().decode())

        current = data["current"]
        condition = WMO_CODES.get(current["weather_code"], f"Code {current['weather_code']}")

        report_lines = [
            f"Current weather in {resolved_name}: {condition}, "
            f"{current['temperature_2m']}°C (feels like {current['apparent_temperature']}°C), "
            f"Humidity: {current['relative_humidity_2m']}%, Wind: {current['wind_speed_10m']} km/h.",
            "3-Day Forecast:",
        ]

        daily = data["daily"]
        for i in range(len(daily["time"])):
            day_date = daily["time"][i]
            day_cond = WMO_CODES.get(daily["weather_code"][i], "Unknown")
            t_min = daily["temperature_2m_min"][i]
            t_max = daily["temperature_2m_max"][i]
            rain_prob = daily["precipitation_probability_max"][i]
            report_lines.append(
                f"- {day_date}: {day_cond}, Min {t_min}°C / Max {t_max}°C, Rain chance: {rain_prob}%"
            )

        return "\n".join(report_lines)
    except Exception as e:
        return f"Weather lookup failed: {e}"