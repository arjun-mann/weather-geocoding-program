from pathlib import Path
import json
import urllib.parse
import urllib.request


# The 'ForwardGeocode' interface consists of the following methods:
#
# def get_result(self, url:str) -> dict:
#     This function takes a URL and returns a Python dictionary representing
#     the parsed JSON response.
#
# def create_coords(self) -> tuple:
#     This function returns tuple coordinates from the ForwardGeocodeAPI object




class ForwardGeocodeAPI:
    def __init__(self, address:str):
        self._address = address
    
    def get_result(self, url:str) -> dict:
        '''This function takes a URL and returns a Python dictionary representing
        the parsed JSON response.
        '''
        response = None
        try:
            request = urllib.request.Request(url, headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/mannas1'})
            response = urllib.request.urlopen(request)
            try:
                json_text = response.read().decode(encoding = 'utf-8')
            except:
                print('FAILED')
                print(str(response.getcode()) + url)
                print('FORMAT')
                exit() 
            
            va = response.getcode()
            if va != 200:
                print('FAILED')
                print(str(response.getcode()) + url)
                print('NOT 200')
                exit()

            return json.loads(json_text)

        finally:
            if response != None:
                response.close()
    
    def custom_url(self) -> str:
        '''This function returns a custom url for the nominatim API'''
        urladdress = self._address.replace(', ','&')
        urladdress = urladdress.replace(' ','+')
        return 'https://nominatim.openstreetmap.org/search?' + 'q=' + urladdress + '&format=json'
    
    def create_coords(self) -> tuple:
        '''This function returns tuple coordinates from the ForwardGeocodeAPI object'''
        url = self.custom_url()
        d = self.get_result(url)[0]
        lat = d['lat']
        lon = d['lon']
        coords = (lat, lon)
        type(coords)
        return coords
        
    def give_credit(self):
        '''Prints credit to the API'''
        print('**Forward geocoding data from OpenStreetMap')
        
class ForwardGeocodeFile:
    def __init__(self, path:Path):
        self._path = path
    
    def get_result(self) -> dict:
        '''This function returns a Python dictionary representing
        the parsed JSON response from self._path.
        '''
        try:
            f = self._path.open('r')
        except:
            print('FAILED')
            print(self._path)
            print('MISSING')
            exit()
            
        try:
            d = json.load(f)
        except:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            exit()
            
        f.close()
        return d
    
    def create_coords(self) -> tuple:
        '''This function returns tuple coordinates from the ForwardGeocodeAPI object'''
        d = self.get_result()[0]
        lat = d['lat']
        lon = d['lon']
        coords = (lat, lon)
        return coords
    
    def give_credit(self):
        '''Prints nothing since a file was used instead of an API'''
        pass
    
    