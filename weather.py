from pathlib import Path
import json
import urllib.parse
import urllib.request
from datetime import timezone
from datetime import datetime

# The 'WeatherForecast' interface consists of the following methods:
#
# def station_coords(self) -> tuple[float, float]
#     Returns a two-element tuple of floats, representing a longitude
#     and latitude representing the average of the points created
#     by the NWS API
#
# def create_dict(self) -> dict:
#     Returns a new dictionary ofthe content within the NWS API
#
# def get_result(self, url:str) -> dict:
#     This function takes a URL and returns a Python dictionary representing
#     the parsed JSON response.
#
# def return_periods(self, urld2:dict, length:int) -> list:
#     Returns a list of periods which each provide weather information for each hour
#
# def get_time(self, period:dict) -> str:
#     Returns a string that represents the UTC time for a given period'''
#
# def celsius_conversion(self, fahrenheit:float) -> float:
#     Returns a celsius float given a fahrenheit float
#
# def humids(self, lperiods:list) -> list:
#     Returns a list relative humidities for a given list of periods
#
# def temps(self, lperiods:list) -> list:
#     Returns a list of temperatures for the given list of periods
#
# def winds(self, lperiods:list) -> list:
#     Returns a list of wind speeds for the given periods
#
# def precips(self, lperiods:list) -> list:
#     Returns a list of precipitations for the given periods
#
# def feels_temp_calculator(self, temp:float, humidity:float, wind:float) -> float:
#     Calculates and returns the feels like temperature given the air temperature, humidity, and wind speed
#
# def maxvalue(self, periodlist:list, unit:str) -> tuple:
#     Returns the maximum value for a certain list of periods for a specific unit/measure
#
# def minvalue(self, periodlist, unit) -> float:
#     Returns the minimum value for a certain list of periods for a specific unit/measure


class WeatherForecastAPI:
    
    def __init__(self, longitude, latitude):
        '''Initializes the WeatherForecastAPI object with a longitude and latitude'''
        self._longitude = longitude
        self._latitude = latitude
        
    def station_coords(self) -> tuple:
        '''Returns the new coordinates as a tuple from the Weather API file'''
        d = self.create_dict()
        lcoords = d['geometry']['coordinates'][0]
        tot = 0
        xtot = 0
        ytot = 0
        for coord in lcoords:
            tot += 1
            xtot += coord[0]
            ytot += coord[1]
        final_coord = (ytot/tot, xtot/tot)
        return final_coord
        
    def create_dict(self) -> dict:
        '''Creates a dictionary of the content within the NWS API'''
        url1 = self.custom_url()
        url1d = (self.get_result(url1))
        url2 = url1d['properties']['forecastHourly']
        url2d = self.get_result(url2)
        return url2d
        
    def custom_url(self) -> str:
        '''Returns a base url string for accessing the first website in NWS API'''
        return 'https://api.weather.gov/points/' + str(self._longitude) + ',' + str(self._latitude)
    
    def get_result(self, url) -> dict:
        '''This function takes a URL and returns a Python dictionary representing
        the parsed JSON response.
        '''
        response = None
        try:
            request = urllib.request.Request(url ,headers = {'User-Agent': '(https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3, mannas1@uci.edu)'})
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
        
    def return_periods(self, urld2:dict, length:int) -> list:
        '''Returns a list of periods which each provide weather information for each hour'''
        dlist = []
        for i in range(length):
            dlist.append(urld2['properties']['periods'][i])
        return dlist
    
    def get_time(self, period:dict) -> str:
        '''Returns a string that represents the UTC time for a given period'''
        time1 = period['startTime']
        datetime1 = datetime.fromisoformat(time1)
        datetime2 = datetime1.astimezone(timezone.utc)
        time2 = str(datetime2.date())+ 'T' + str(datetime2.time()) + 'Z'
        return time2
    
    def celsius_conversion(self, fahrenheit:float) -> float:
        '''Returns a celsius float given a fahrenheit float'''
        celsius = (fahrenheit - 32) * 5/9
        return celsius
      
    def humids(self, lperiods:list) -> list:
        '''Returns a list relative humidities for a given list of periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['relativeHumidity']['value'])
        return l2
    
    def temps(self, lperiods:list) -> list:
        '''Returns a list of temperatures for the given periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['temperature'])
        return l2
    
    def winds(self, lperiods:list) -> list:
        '''Returns a list of wind speeds for the given periods'''
        l2 = []
        for period in lperiods:
            full_entry = period['windSpeed']
            val_end_index = full_entry.index(' ')
            wind_val = float(full_entry[:val_end_index])
            l2.append(wind_val)
        return l2
    
    def precips(self, lperiods:list) -> list:
        '''Returns a list of precipitations for the given periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['probabilityOfPrecipitation']['value'])
        return l2
    
    def feels_temp_calculator(self, temp:float, humidity:float, wind:float) -> float:
        '''Calculates and returns the feels like temperature given the air temperature, humidity, and wind speed'''
        if temp >= 68:
            feels_temp = -42.379 + (2.04901523*temp) + (10.14333127*humidity) + (-0.22475541*temp*humidity) + (-0.00683783*(temp**2)) + (-0.05481717*(humidity**2)) + (0.00122874*(temp**2)*humidity) + (0.00085282*temp*(humidity**2)) + (-0.00000199*(temp**2)*(humidity**2))
        if temp <= 50 and wind > 3:
            feels_temp = 35.74 + (0.6215*temp) + (-35.75*(wind**0.16)) + (0.4275*temp*(wind**0.16))
        else:
            feels_temp = temp
        return feels_temp
    
    def feels(self, lperiods:list) -> list:
        '''Returns a list of feel like temperatures for the given periods'''
        l2 = []
        for period in lperiods:
            temp = period['temperature']
            humid = period['relativeHumidity']['value']
            full_wind = period['windSpeed']
            wind_end_index = full_wind.index(' ')
            wind = float(full_wind[:wind_end_index])
            l2.append(self.feels_temp_calculator(temp, humid, wind))
        return l2

    
    def maxvalue(self, periodlist:list, unit:str) -> tuple:
        '''Returns the maximum value for a certain list of periods for a specific unit/measure'''
        if unit == 'TEMPERATURE AIR':
            templist = self.temps(periodlist)
        elif unit == 'TEMPERATURE FEELS':
            templist = self.feels(periodlist)
        elif unit == 'WIND':
            templist = self.winds(periodlist)
        elif unit == 'HUMIDITY':
            templist = self.humids(periodlist)
        elif unit == 'PRECIPITATION':
            templist = self.precips(periodlist)
        max = templist[0]
        for i in range(len(templist)):
            if templist[i] > max:
                max = templist[i]
        for i in range(len(templist)):
            if templist[i] == max:
                return (self.get_time(periodlist[i]), max)

    def minvalue(self, periodlist, unit) -> float:
        '''Returns the minimum value for a certain list of periods for a specific unit/measure'''
        if unit == 'TEMPERATURE AIR':
            templist = self.temps(periodlist)
        elif unit == 'TEMPERATURE FEELS':
            templist = self.feels(periodlist)
        elif unit == 'WIND':
            templist = self.winds(periodlist)
        elif unit == 'HUMIDITY':
            templist = self.humids(periodlist)
        elif unit == 'PRECIPITATION':
            templist = self.precips(periodlist)
        min = templist[0]
        for i in range(len(templist)):
            if templist[i] < min:
                min = templist[i]
        for i in range(len(templist)):
            if templist[i] == min:
                return (self.get_time(periodlist[i]), min)
        
    def give_credit(self):
        print('**Real-time weather data from National Weather Service, United States Department of Commerce')
        

class WeatherForecastFile:
    def __init__(self, path:Path):
        self._path = path
    
    def station_coords(self) -> tuple:
        '''Returns the new coordinates as a tuple from the Weather API file'''
        d = self.get_result()
        lcoords = d['geometry']['coordinates'][0]
        tot = 0
        xtot = 0
        ytot = 0
        for coord in lcoords:
            tot += 1
            xtot += coord[0]
            ytot += coord[1]
        final_coord = (ytot/tot, xtot/tot)
        return final_coord
    
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
    
    def return_periods(self, d, length) -> list:
        '''returns a list where each element is the dictionary for the indexed hour'''
        dlist = []
        for i in range(length):
            dlist.append(d['properties']['periods'][i])
        return dlist
        
    def get_time(self, period:dict) -> str:
        '''Returns the time in UTC for the provided period'''
        time1 = period['startTime']
        datetime1 = datetime.fromisoformat(time1)
        datetime2 = datetime1.astimezone(timezone.utc)
        time2 = str(datetime2.date())+ 'T' + str(datetime2.time()) + 'Z'
        return time2
    
    def celsius_conversion(self, fahrenheit) -> float:
        '''Returns the conversion of a given fahrenheit value to celsius'''
        celsius = (fahrenheit - 32) * 5/9
        return celsius
    
    def humids(self, lperiods:list) -> list:
        '''Returns a list of relative humidities for the given periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['relativeHumidity']['value'])
        return l2
    
    def temps(self, lperiods:list) -> list:
        '''Returns a list of temperatures for the given periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['temperature'])
        return l2
    
    def winds(self, lperiods:list) -> list:
        '''Returns a list of wind speeds for the given periods '''
        l2 = []
        for period in lperiods:
            full_entry = period['windSpeed']
            val_end_index = full_entry.index(' ')
            wind_val = float(full_entry[:val_end_index])
            l2.append(wind_val)
        return l2
    
    def precips(self, lperiods:list) -> list:
        '''Returns a list of precipitations for the given periods'''
        l2 = []
        for period in lperiods:
            l2.append(period['probabilityOfPrecipitation']['value'])
        return l2
    
    def feels_temp_calculator(self, temp:float, humidity:float, wind:float) -> float:
        '''Calculates and returns the feels like temperature given the air temperature, humidity, and wind speed'''
        if temp >= 68:
            feels_temp = -42.379 + (2.04901523*temp) + (10.14333127*humidity) + (-0.22475541*temp*humidity) + (-0.00683783*(temp**2)) + (-0.05481717*(humidity**2)) + (0.00122874*(temp**2)*humidity) + (0.00085282*temp*(humidity**2)) + (-0.00000199*(temp**2)*(humidity**2))
        if temp <= 50 and wind > 3:
            feels_temp = 35.74 + (0.6215*temp) + (-35.75*(wind**0.16)) + (0.4275*temp*(wind**0.16))
        else:
            feels_temp = temp
        return feels_temp
    
    def feels(self, lperiods) -> list:
        '''Returns a list of feel like temperatures for the given periods'''
        l2 = []
        for period in lperiods:
            temp = period['temperature']
            humid = period['relativeHumidity']['value']
            full_wind = period['windSpeed']
            wind_end_index = full_wind.index(' ')
            wind = float(full_wind[:wind_end_index])
            l2.append(self.feels_temp_calculator(temp, humid, wind))
        return l2
    
    def maxvalue(self, periodlist, unit) -> tuple:
        '''Returns the maximum value for a certain list of periods for a specific unit/measure'''
        if unit == 'TEMPERATURE AIR':
            templist = self.temps(periodlist)
        elif unit == 'TEMPERATURE FEELS':
            templist = self.feels(periodlist)
        elif unit == 'WIND':
            templist = self.winds(periodlist)
        elif unit == 'HUMIDITY':
            templist = self.humids(periodlist)
        elif unit == 'PRECIPITATION':
            templist = self.precips(periodlist)
        max = templist[0]
        for i in range(len(templist)):
            if templist[i] > max:
                max = templist[i]
        for i in range(len(templist)):
            if templist[i] == max:
                return (self.get_time(periodlist[i]), max)
        
    def minvalue(self, periodlist, unit) -> float:
        '''Returns the minimum value for a certain list of periods for a specific unit/measure'''
        if unit == 'TEMPERATURE AIR':
            templist = self.temps(periodlist)
        elif unit == 'TEMPERATURE FEELS':
            templist = self.feels(periodlist)
        elif unit == 'WIND':
            templist = self.winds(periodlist)
        elif unit == 'HUMIDITY':
            templist = self.humids(periodlist)
        elif unit == 'PRECIPITATION':
            templist = self.precips(periodlist)
        min = templist[0]
        for i in range(len(templist)):
            if templist[i] < min:
                min = templist[i]
        for i in range(len(templist)):
            if templist[i] == min:
                return (self.get_time(periodlist[i]), min)
            
    def give_credit(self):
        '''Prints nothing since a file was used instead of an API'''
        pass
            

#Temporary below here:
if __name__ == '__main__':
    # wa = WeatherForecastAPI(33.6432,-117.8419)
    # d = wa.create_dict()
    # lp = wa.return_periods(d, 3)
    # print(wa.feels(lp, 'MIN'))
    ...
    
    
    # p = Path('nws_hourly.json')
    # wf = WeatherForecastFile(p)
    # d = wf.get_result_file()
    # lp = wf.return_periods(d, 3)
    # print(wf.feels(lp, 'MIN'))

    