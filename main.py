import time
import glob
import sys
import ipgetter
import requests
import forecastio
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

api_key = 'adc320c63105603c790551b8bf78ccad'


#this is where out logic is goin to live
def main():
	#In order to get weather data we need to know where we are
	#we'll do this using our ip address
	matrix = display_setup()
	json_location = get_location()
	lat = str(json_location['latitude'])
	lon = str(json_location['longitude'])
	#get_weather_data(lat,lon)
	#this logic will project will probably be a loop
	for x in range(10):
                display_animation(matrix,"rain",.3)


def get_location():
	ip = ipgetter.myip()
	url = 'http://freegeoip.net/json/'+ip
	r = requests.get(url)
	return r.json();

def get_weather_data(lat,lon):
	forecast = forecastio.load_forecast(api_key, lat, lon)
	hourly = forecast.hourly()
	print hourly.data[0].precipProbability

def display_animation(matrix, weather, speed):
        for filename in sorted(glob.glob(weather+ "/*")):
                im = Image.open(filename)
                matrix.SetImage(im.convert('RGB'))
                time.sleep(speed)
        

def display_setup():
	options = RGBMatrixOptions()
	options.rows = 16
	options.chain_length = 1
	options.parallel = 1
	options.hardware_mapping  = 'regular'
	matrix = RGBMatrix(options = options)
	return matrix

main()
