import time
import glob
import sys
import ipgetter
import requests
import forecastio
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


api_key = 'YourApiKey'
im_now = Image.open('now.png')
im_today = Image.open('today.png')

#this is where out logic is goin to live
def main():
	#In order to get weather data we need to know where we are
	#we'll do this using our ip address
	matrix = display_setup()
	json_location = get_location()
	lat = str(json_location['latitude'])
	lon = str(json_location['longitude'])
	forecast = get_weather_data(lat,lon)
	currently = forecast.currently()
	daily = forecast.daily()
	print currently.icon
	print daily.data[2].icon
	print currently.apparentTemperature
	for x in range(10000):
                '''matrix.Clear()
                matrix.SetImage(im_now.convert('RGB'))
                time.sleep(2)
                matrix.Clear()
                animation_by_icon(currently.icon,matrix)
                matrix.Clear()
                matrix.SetImage(im_today.convert('RGB'))
                time.sleep(2)
                matrix.Clear()
                animation_by_icon(daily.data[2].icon,matrix)'''
        
		clear_day(matrix)
		rain(matrix)
		snow(matrix)
		cloudy(matrix)
	
	
	
        

def clear_day(matrix):
        for x in range(10):
                display_animation(matrix,"sun",.2)

def rain(matrix):
        for x in range(10):
                display_animation(matrix, "rain", .2)

def snow(matrix):
        for x in range(10):
                display_animation(matrix, "snow", .2)

def cloudy(matrix):
        for x in range(10):
                display_animation(matrix, "cloudy", .2)

def get_location():
	ip = ipgetter.myip()
	url = 'http://freegeoip.net/json/'+ip
	r = requests.get(url)
	return r.json();

def get_weather_data(lat,lon):
	forecast = forecastio.load_forecast(api_key, lat, lon)
	return forecast
	#hourly = forecast.hourly()
	#print hourly.data[0].precipProbability

def animation_by_icon(icon, matrix):
        if icon == "clear_day":
                clear_day(matrix)
        elif icon == "rain":
                rain(matrix)
        elif icon == "snow":
                snow(matrix)
        elif icon == "cloudy":
                cloudy(matrix)
        else:
                clear_day(matrix)

def display_animation(matrix, weather, speed):
        for filename in sorted(glob.glob(weather+ "/*")):
                im = Image.open(filename)
                matrix.SetImage(im.convert('RGB'))
                time.sleep(speed)
                
def display_text(matrix, text, speed):
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width

        for x in range(100):
                offscreen_canvas.Clear()
                len = graphics.VerticalDrawText(offscreen_canvas, font, pos, 10, textColor, text)
                pos -= 1
                if (pos + len < 0):
                        pos = offscreen_canvas.width

                time.sleep(0.05)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        matrix.Clear()

def display_setup():
	options = RGBMatrixOptions()
	options.rows = 16
	options.chain_length = 1
	options.parallel = 1
	options.hardware_mapping  = 'regular'
	matrix = RGBMatrix(options = options)
	return matrix

while True:
        main()
