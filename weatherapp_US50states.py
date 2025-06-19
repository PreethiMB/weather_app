#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

API_KEY = '12efc13cfe9b01e34b6f19f0e2c6b33b'

cities = [
    {"name": "Montgomery, AL", "lat": 32.3668, "lon": -86.3000},
    {"name": "Juneau, AK", "lat": 58.3019, "lon": -134.4197},
    {"name": "Phoenix, AZ", "lat": 33.4484, "lon": -112.0740},
    {"name": "Little Rock, AR", "lat": 34.7465, "lon": -92.2896},
    {"name": "Sacramento, CA", "lat": 38.5816, "lon": -121.4944},
    {"name": "Denver, CO", "lat": 39.7392, "lon": -104.9903},
    {"name": "Hartford, CT", "lat": 41.7658, "lon": -72.6734},
    {"name": "Dover, DE", "lat": 39.1582, "lon": -75.5244},
    {"name": "Tallahassee, FL", "lat": 30.4383, "lon": -84.2807},
    {"name": "Atlanta, GA", "lat": 33.7490, "lon": -84.3880},
    {"name": "Honolulu, HI", "lat": 21.3069, "lon": -157.8583},
    {"name": "Boise, ID", "lat": 43.6150, "lon": -116.2023},
    {"name": "Springfield, IL", "lat": 39.7817, "lon": -89.6501},
    {"name": "Indianapolis, IN", "lat": 39.7684, "lon": -86.1581},
    {"name": "Des Moines, IA", "lat": 41.5868, "lon": -93.6250},
    {"name": "Topeka, KS", "lat": 39.0489, "lon": -95.6770},
    {"name": "Frankfort, KY", "lat": 38.2009, "lon": -84.8733},
    {"name": "Baton Rouge, LA", "lat": 30.4515, "lon": -91.1871},
    {"name": "Augusta, ME", "lat": 44.3106, "lon": -69.7795},
    {"name": "Annapolis, MD", "lat": 38.9784, "lon": -76.4922},
    {"name": "Boston, MA", "lat": 42.3601, "lon": -71.0589},
    {"name": "Lansing, MI", "lat": 42.7325, "lon": -84.5555},
    {"name": "Saint Paul, MN", "lat": 44.9537, "lon": -93.0900},
    {"name": "Jackson, MS", "lat": 32.2988, "lon": -90.1848},
    {"name": "Jefferson City, MO", "lat": 38.5767, "lon": -92.1735},
    {"name": "Helena, MT", "lat": 46.5891, "lon": -112.0391},
    {"name": "Lincoln, NE", "lat": 40.8136, "lon": -96.7026},
    {"name": "Carson City, NV", "lat": 39.1638, "lon": -119.7674},
    {"name": "Concord, NH", "lat": 43.2081, "lon": -71.5376},
    {"name": "Trenton, NJ", "lat": 40.2171, "lon": -74.7429},
    {"name": "Santa Fe, NM", "lat": 35.6870, "lon": -105.9378},
    {"name": "Albany, NY", "lat": 42.6526, "lon": -73.7562},
    {"name": "Raleigh, NC", "lat": 35.7796, "lon": -78.6382},
    {"name": "Bismarck, ND", "lat": 46.8083, "lon": -100.7837},
    {"name": "Columbus, OH", "lat": 39.9612, "lon": -82.9988},
    {"name": "Oklahoma City, OK", "lat": 35.4676, "lon": -97.5164},
    {"name": "Salem, OR", "lat": 44.9429, "lon": -123.0351},
    {"name": "Harrisburg, PA", "lat": 40.2732, "lon": -76.8867},
    {"name": "Providence, RI", "lat": 41.8240, "lon": -71.4128},
    {"name": "Columbia, SC", "lat": 34.0007, "lon": -81.0348},
    {"name": "Pierre, SD", "lat": 44.3683, "lon": -100.3509},
    {"name": "Nashville, TN", "lat": 36.1627, "lon": -86.7816},
    {"name": "Austin, TX", "lat": 30.2672, "lon": -97.7431},
    {"name": "Salt Lake City, UT", "lat": 40.7608, "lon": -111.8910},
    {"name": "Montpelier, VT", "lat": 44.2601, "lon": -72.5754},
    {"name": "Richmond, VA", "lat": 37.5407, "lon": -77.4360},
    {"name": "Olympia, WA", "lat": 47.0379, "lon": -122.9007},
    {"name": "Charleston, WV", "lat": 38.3498, "lon": -81.6326},
    {"name": "Madison, WI", "lat": 43.0731, "lon": -89.4012},
    {"name": "Cheyenne, WY", "lat": 41.1399, "lon": -104.8202}
]

@st.cache_data(ttl=600)
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={city['lat']}&lon={city['lon']}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "City": city['name'],
            "Lat": city['lat'],
            "Lon": city['lon'],
            "Rainfall (mm)": data.get("rain", {}).get("1h", 0),
            "Temperature (C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"]
        }
    else:
        return None

def fetch_aqi(city):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={city['lat']}&lon={city['lon']}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        aqi = data['list'][0]['main']['aqi']  # AQI scale 1 (Good) to 5 (Very Poor)
        return aqi
    else:
        return None

def aqi_description(aqi):
    return {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }.get(aqi, "Unknown")

def get_color(temp_c):
    if temp_c < 0:
        return 'blue'
    elif 0 <= temp_c < 10:
        return 'lightblue'
    elif 10 <= temp_c < 20:
        return 'green'
    elif 20 <= temp_c < 30:
        return 'orange'
    else:
        return 'red'

st.title("Live Weather & Air Quality Map - USA State Capitals")

weather_data = []
for city in cities:
    w = fetch_weather(city)
    aqi = fetch_aqi(city)
    if w and aqi:
        w['AQI'] = aqi
        w['AQI_Desc'] = aqi_description(aqi)
        weather_data.append(w)

df = pd.DataFrame(weather_data)
st.dataframe(df)

map_center = [39.8283, -98.5795]
# Create Folium map with different basemap (Stamen Toner)
map_center = [39.8283, -98.5795]
#m = folium.Map(location=map_center, zoom_start=4, tiles='Stamen Toner')
m = folium.Map(
    location=[39.8283, -98.5795],
    zoom_start=4,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery"
)


for city in weather_data:
    color = get_color(city['Temperature (C)'])
    tooltip_text = f"{city['City']} - {city['Temperature (C)']} °C - AQI: {city['AQI_Desc']}"
    popup_text = (
        f"<b>{city['City']}</b><br>"
        f"Temperature: {city['Temperature (C)']} °C<br>"
        f"Humidity: {city['Humidity (%)']}%<br>"
        f"Rainfall (last 1h): {city['Rainfall (mm)']} mm<br>"
        f"AQI: {city['AQI']} ({city['AQI_Desc']})"
    )
    folium.CircleMarker(
        location=[city['Lat'], city['Lon']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=tooltip_text,
        popup=popup_text
    ).add_to(m)

st_folium(m, width=700, height=500)


# In[ ]:




