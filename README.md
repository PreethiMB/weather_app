"USA Live Weather and Air QUality Map"

This interactive web app displays real-time weather and air quality data for all 50 U.S. state capitals. It was created as a practice project to showcase data visualization skills using Streamlit and Folium.
**Features
 - Interactive map wuth color-coded markers
 - Live weather data: Temperature, Rainfall, Humidity (last 1 hour)
 - Real-time Air Quality Index (AQI)
 - Hover tooltips for instant weather info
 - Data table showing all state-level weather details

Tech Stack
- Python 3
- Streamlit: for building web app
- Folium: for map visualization
- OpenWeatherMap API: for live weather and air quality data
- Pandas: for data handling
- streamlit-folium: to display folium maps in Streamlit

  
bash
# Clone the repository
git clone https://github.com/your-username/weather_app.git
cd weather_app

# (Optional) Create a virtual environment
conda create -n streamlit-env python=3.10
conda activate streamlit-env

# Install required packages
pip install -r requirements.txt

# Run the Streamlit app
streamlit run weather_app.py
