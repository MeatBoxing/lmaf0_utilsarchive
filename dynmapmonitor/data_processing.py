import requests
import math

def fetch_player_data():
    try:
        url = "urlhere"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            players = data.get("players", [])
            server_time = data.get("servertime")
            return players, server_time
        else:
            print(f"Error: {response.status_code}")
            return [], None
    except Exception as e:
        print(f"Error: {e}")
        return [], None

def format_time(hours, minutes):
    return "{:02d}:{:02d}".format(hours, minutes)

def get_time(servertime):
    total_minutes = int((servertime + 6000) % 24000 / 1000 * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return hours, minutes

def get_sun_moon_position(servertime):
    sunangle = 0
    if servertime > 23100 or servertime < 12900:
        movedtime = servertime + 900
        movedtime = movedtime - 24000 if movedtime >= 24000 else movedtime
        sunangle = (movedtime / 27600) * 2 * math.pi
    else:
        movedtime = servertime - 12900
        sunangle = math.pi + (movedtime / 20400) * 2 * math.pi

    moonangle = sunangle + math.pi

    sun_x = -50 * math.cos(sunangle)
    sun_y = -50 * math.sin(sunangle)
    moon_x = -50 * math.cos(moonangle)
    moon_y = -50 * math.sin(moonangle)

    return sun_x, sun_y, moon_x, moon_y
