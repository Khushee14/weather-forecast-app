import streamlit as st
import requests
from PIL import Image
from streamlit_lottie import st_lottie

# Page configuration
st.set_page_config(page_title="🌦️ Weather App", layout="centered", page_icon="🌤️")

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .stTextInput>div>div>input {
            border: 2px solid #1f77b4;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1.5em;
        }
        .weather-block {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🌦️ Real-Time Weather Forecast")
st.markdown("Enter a city name below to get the current and next-day weather forecast:")

# Input box
city = st.text_input("📍 City Name", "Delhi")

# Button
if st.button("🔍 Get Weather"):
    with st.spinner("Fetching weather data..."):
        try:
            response = requests.get(
                "https://weather-backend-harshit-g7crage4frb3czbm.centralindia-01.azurewebsites.net/api/weather",
                params={"city": city}
            )
            data = response.json()

            if "error" in data:
                st.error(f"❌ {data['error']}")
            else:
                today = data["today"]
                st.markdown(f"### ☀️ Today's Weather in {city.title()}")
                with st.container():
                    st.markdown('<div class="weather-block">', unsafe_allow_html=True)
                    st.image(f"http://openweathermap.org/img/wn/{today['icon']}@2x.png", width=100)
                    st.write(f"🌡️ **Temperature:** `{today['temperature']}°C`")
                    st.write(f"⛅ **Condition:** `{today['description'].title()}`")
                    st.write(f"💧 **Humidity:** `{today['humidity']}%`")
                    st.write(f"🌬️ **Wind Speed:** `{today['wind_speed']} m/s`")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Tomorrow
                tomorrow = data.get("tomorrow")
                if tomorrow:
                    st.markdown(f"### 🌤️ Forecast for Tomorrow")
                    with st.container():
                        st.markdown('<div class="weather-block">', unsafe_allow_html=True)
                        st.image(f"http://openweathermap.org/img/wn/{tomorrow['icon']}@2x.png", width=100)
                        st.write(f"🌡️ **Temperature:** `{tomorrow['temperature']}°C`")
                        st.write(f"⛅ **Condition:** `{tomorrow['description'].title()}`")
                        st.write(f"💧 **Humidity:** `{tomorrow['humidity']}%`")
                        st.write(f"🌬️ **Wind Speed:** `{tomorrow['wind_speed']} m/s`")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Tomorrow's forecast is not available at the moment.")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
