from pathlib import Path
import json
import urllib.parse
import urllib.request

# The 'ReverseGeocode' interface consists of the following methods:
#
# def get_result(self, url:str) -> dict:
#     This function takes a URL and returns a Python dictionary representing
#     the parsed JSON response.
#
# def create_description(self) -> str:
#     Returns a description from analyzing provided coordinates'''


class ReverseGeocodeAPI:
    
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon
        
    def get_result(self, url) -> dict:
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
        return 'https://nominatim.openstreetmap.org/reverse?lat=' + str(self._lat) + '&lon=' + str(self._lon) + '&format=json'
    
    def give_credit(self):
        '''Prints credit to the API'''
        print('**Reverse geocoding data from OpenStreetMap')
        
    def create_description(self) -> str:
        '''Returns a description from analyzing provided coordinates'''
        url = self.custom_url()
        d = self.get_result(url)
        desc = d['display_name']
        return desc
        
        
class ReverseGeocodeFile:
    def __init__(self, path:Path):
        self._path = path
        
    def get_result_file(self) -> dict:
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
            print('MISSING')
            exit()
            
        f.close()
        return d
    
    def create_desc(self) -> str:
        '''Returns a description from analyzing provided coordinates'''
        d = self.get_result_file()
        desc = d['display_name']
        return desc
    
    def give_credit(self):
        '''Prints nothing since a file was sued instead of an API'''
        pass
        


        
        
        
        
        
        

