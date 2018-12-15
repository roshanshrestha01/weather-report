import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WEATHER_BASE_API = 'http://api.openweathermap.org/data/2.5/forecast?appid=c96fdc2a77cbd10dd95cae3273cd8174&units=metric&q='
WEATHER_SINGLE_BASE_API = 'https://api.openweathermap.org/data/2.5/weather?appid=c96fdc2a77cbd10dd95cae3273cd8174&units=metric&q='

TIME_ZONE = 'Asia/Kathmandu'

CSV_DRUMP_DIR = os.path.join(BASE_DIR, 'csv')


