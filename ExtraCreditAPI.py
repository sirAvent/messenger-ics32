import urllib, json
from urllib import request,error



class Dog:
    """
    The Dog class returns an
    object containing an image of a dog and its breed.
    """
    def __init__(self):
        self.picture = ''
        self.breed = ''
        try:
            url = f"https://dog.ceo/api/breeds/image/random"
            dog_obj = _download_url(url)
            if dog_obj is not None:
                self.picture = dog_obj['message']
                self.breed = getBreed(dog_obj['message'])
        except:
            print('Error. Connection was lost1')


   
    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude    
        :returns: The transcluded message
        '''
        if '@extracredit' in message:
            message = message.replace('@extracredit', self.picture)
        if '@breed' in message:
            message = message.replace('@breed', self.breed)
        return message


def getBreed(dogURL):
    """Accept the URL for a dog image from the API and returns the breed."""
    breedInd = (dogURL.index('breeds'))
    reverse = dogURL[::-1]
    slash = (reverse.index('/'))
    new = dogURL[breedInd + 7:-slash - 1]
    breedString =(new.split('-'))
    breed = ''
    for wordInd, word in enumerate(breedString[::-1]):
        if wordInd == 0:
            breed += word
        else:
            breed += ' ' + word
    return breed


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
    url = f"https://dog.ceo/api/breeds/image/random"
    dog_obj = _download_url(url)
    if dog_obj is not None:
        print(dog_obj['message'])


if __name__ == '__main__':
    main()
