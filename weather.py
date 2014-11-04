from infosys import infosys
import requests
import argparse

cityId = '5137454'

url = 'http://api.openweathermap.org/data/2.5/weather?id=' + cityId

infosysKey = 'fe3e9d5c-8068-42d5-835c-5f01eaf0271a'

def currentWeather():
    global url, infosysKey
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
    
        info = infosys(infosysKey)
        
        temp = convertKelvinToF(json['main']['temp'])#space 2
        humidity = json['main']['humidity']#space 3
        windSpeed = json['wind']['speed']#space 4
        condition = json['weather'][0]['description']#space 5 
        info.addString(2, temp)
        info.addString(3, humidity)
        info.addString(4, windSpeed)
        info.addString(5, condition)

def setup():
    global infosysKey
    info = infosys(infosysKey)
    info.addMultiText(0, ['Current Weather', '<STRINGFILE:5>  <STRINGFILE:2><PICTUREFILE:1>F  <STRINGFILE:3>% Humidity  Wind <STRINGFILE:4> MPH'], ['SNOW', 'ROTATE'])
    info.addPicture(1, ['0110', '1001', '1001', '0110', '0000', '0000', '0000'])

def convertKelvinToF(temp):
    return ((temp - 273.15) * 1.8)  + 32

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='InfoSys weather script')
    parser.add_argument('-s', '--setup', help = 'Run the setup', action='store_true')
    args = parser.parse_args()
    if args.setup:
        setup()
    currentWeather()
