import urllib, json
from urllib import request,error


class LastFM:
    """
    The lastFM class accepts page and limit information and API key as parameters
    and returns an object containing the top Artist Chart.
    """
    def __init__(self, page='', limit='', apikey=None):
        self.apikey = apikey # REQUIRED
        self.page = page # OPTIONAL
        self.limit = limit # OPTIONAL
        self.chart = ''
        self.topArtist = ''
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={apikey}&page={page}&limit={limit}&format=json"
            lastFM_obj = _download_url(url)
            if lastFM_obj is not None:
                topArtistList = []
                for artist in lastFM_obj['artists']['artist']:
                    topArtistList.append(artist['name'])
                self.chart = topArtistList
                self.topArtist = topArtistList[0]
        except:
            print('Failed to download contents of URL')

            
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
        if '@lastfm' in message:
            message = message.replace('@lastfm', self.topArtist)
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
    page = "2"
    limit = "10"
    apikey = "YOUR API HERE"
    url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={apikey}&page={page}&limit={limit}&format=json"

    lastFM_obj = _download_url(url)
    if lastFM_obj is not None:
        ranking = 1
        for artist in lastFM_obj['artists']['artist']:
            print(str(ranking) + '.', artist['name'])
            ranking += 1


if __name__ == '__main__':
    main()
    
#3ceeebef4e84ac6acfa739ad3338c196
#http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=YOUR_API_KEY&format=json
