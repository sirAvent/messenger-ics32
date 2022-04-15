import urllib, json
from urllib import request,error
from datetime import datetime

#85b35a1129e8d147851f71ecde8bc02e - The API key


class OpenWeather:
    """
    The OpenWeather class accepts location information and API key as parameters
    and returns an object containing weather data.
    """
    def __init__(self, zipcode=None, ccode=None, apikey=None):
        self.zipcode = zipcode # REQUIRED
        self.ccode = ccode # REQUIRED
        self.apikey = apikey # REQUIRED
        self.temperature = ''
        self.high_temperature = ''
        self.low_temperature = ''
        self.humidity = ''
        self.pressure = ''
        self.longitude = ''
        self.latitude = ''
        self.description = ''
        self.sunset = ''
        self.sunrise = ''
        self.city = ''
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{ccode}&appid={self.apikey}&units=imperial"
            weather_obj = _download_url(url)
            if weather_obj is not None:
                self.temperature = weather_obj['main']['temp']
                self.high_temperature = weather_obj['main']['temp_max']
                self.low_temperature = weather_obj['main']['temp_min']
                self.humidity = weather_obj['main']['humidity']
                self.pressure = weather_obj['main']['pressure']
                self.longitude = weather_obj['coord']['lon']
                self.latitude = weather_obj['coord']['lat']
                self.description = weather_obj['weather'][0]['description']
                self.sunset = datetime.utcfromtimestamp(weather_obj['sys']['sunset']).strftime('%H:%M:%S GMT')
                self.sunrise = datetime.utcfromtimestamp(weather_obj['sys']['sunrise']).strftime('%H:%M:%S GMT')
                self.city = weather_obj['name']       
        except:
            print('Error. Connection was lost')

    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
           
        '''
        self.apikey = apikey



    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude    
        :returns: The transcluded message
        '''
        if '@weather' in message:
            message = message.replace('@weather', self.description)
        if '@temperature' in message:
            message = message.replace('@temperature', str(self.temperature))
        
        return message


def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))

    finally:
        if response != None:
            response.close()
    
    return r_obj

def main() -> None:
    zip = "91706"
    ccode = "US"
    apikey = "85b35a1129e8d147851f71ecde8bc02e"
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"
    
    weather_obj = _download_url(url)
    if weather_obj is not None:
        print(weather_obj['weather'][0]['description'])
        print(weather_obj)


if __name__ == '__main__':
    main()
