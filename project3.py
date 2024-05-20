from pathlib import Path
import json
import urllib.parse
import urllib.request

import weather
import forwardgeocode
import reversegeocode

# Bren Hall, Ring Mall, University of California, Irvine, Irvine, Orange County, California, 92697, United States

def feels_temp_calculator(temp:float, humidity:float, wind:float) -> float:
    if temp >= 68:
        feels_temp = -42.379 + (2.04901523*temp) + (10.14333127*humidity) + (-0.22475541*temp*humidity) + (-0.00683783*(temp**2)) + (-0.05481717*(humidity**2)) + (0.00122874*(temp**2)*humidity) + (0.00085282*temp*(humidity**2)) + (-0.00000199*(temp**2)*(humidity**2))
    if temp <= 50 and wind > 3:
        feels_temp = 35.74 + (0.6215*temp) + (-35.75*(wind**0.16)) + (0.4275*temp*(wind**0.16))
    else:
        feels_temp = temp
    return feels_temp

def temp_air_method(weather_object, wdict, scale, length, limit):
    period_list = weather_object.return_periods(wdict, length)
    if limit == 'MAX':
        final_temp = weather_object.maxvalue(period_list, 'TEMPERATURE AIR')
    if limit == 'MIN':
        final_temp = weather_object.minvalue(period_list, 'TEMPERATURE AIR')
    if scale == 'C':
        final_temp = (final_temp[0], weather_object.celsius_conversion(final_temp[1]))
    num = '{n:.4f}'.format(n = final_temp[1])
    final_temp = (final_temp[0], num)
    return final_temp

def temp_feels_method(weather_object, wdict, scale, length, limit):
    period_list = weather_object.return_periods(wdict, length)
    if limit == 'MAX':
        final_temp = weather_object.maxvalue(period_list, 'TEMPERATURE FEELS')
    if limit == 'MIN':
        final_temp = weather_object.minvalue(period_list, 'TEMPERATURE FEELS')
    if scale == 'C':
        final_temp = (final_temp[0], weather_object.celsius_conversion(final_temp[1]))
    num = '{n:.4f}'.format(n = final_temp[1])
    final_temp = (final_temp[0], num)
    return final_temp
        
def wind_method(weather_object, wdict, length, limit):
    period_list = weather_object.return_periods(wdict, length)
    if limit == 'MAX':
        final_wind = weather_object.maxvalue(period_list, 'WIND')
    if limit == 'MIN':
        final_wind = weather_object.minvalue(period_list, 'WIND')
    num = '{n:.4f}'.format(n = final_wind[1])
    final_wind = (final_wind[0], num)
    return final_wind       

def humid_method(weather_object, wdict, length, limit):
    period_list = weather_object.return_periods(wdict, length)
    if limit == 'MAX':
        final_humid = weather_object.maxvalue(period_list, 'HUMIDITY')
    if limit == 'MIN':
        final_humid = weather_object.minvalue(period_list, 'HUMIDITY')
    num = '{n:.4f}%'.format(n = final_humid[1])
    final_humid = (final_humid[0], num)
    return final_humid  

def precip_method(weather_object, wdict, length, limit):
    period_list = weather_object.return_periods(wdict, length)
    if limit == 'MAX':
        final_precip = weather_object.maxvalue(period_list, 'PRECIPITATION')
    if limit == 'MIN':
        final_precip = weather_object.minvalue(period_list, 'PRECIPITATION')
    num = '{n:.4f}%'.format(n = final_precip[1])
    final_precip = (final_precip[0], num)
    return final_precip
            
def run():
    fline = input()
    og_coords = None
    fa = None
    if fline.startswith('TARGET NOMINATIM'):
        description = fline[17:]
        fa = forwardgeocode.ForwardGeocodeAPI(description)
        og_coords = fa.create_coords()
    elif fline.startswith('TARGET FILE'):
        filename = fline[12:]
        p = Path(filename)
        fa = forwardgeocode.ForwardGeocodeFile(p)
        og_coords = fa.create_coords()
    line2 = input()
    wa = None
    weatherdict = None
    if line2.startswith('WEATHER NWS'):
        wa = weather.WeatherForecastAPI(og_coords[0],og_coords[1]) #replace with input coords
        weatherdict = wa.create_dict()
    elif line2.startswith('WEATHER FILE'):
        filename = line2[13:]
        p = Path(filename)
        wa = weather.WeatherForecastFile(p)
        weatherdict = wa.get_result()
    report_location = wa.station_coords()
    command = ''
    outputs = []
    while command.startswith('NO MORE QUERIES') == False:
        command = input('')
        if command.startswith('TEMPERATURE AIR'):
            allfields = command[16:]
            lfields = allfields.split(' ')
            outputs.append(temp_air_method(wa, weatherdict, lfields[0], int(lfields[1]), lfields[2]))
        elif command.startswith('TEMPERATURE FEELS'):
            allfields = command[18:]
            lfields = allfields.split(' ')  
            outputs.append(temp_feels_method(wa, weatherdict, lfields[0], int(lfields[1]), lfields[2]))
        elif command.startswith('HUMIDITY'):
            allfields = command[9:]
            lfields = allfields.split(' ')
            outputs.append(humid_method(wa, weatherdict, int(lfields[0]), (lfields[1])))
        elif command.startswith('WIND'):
            allfields = command[5:]
            lfields = allfields.split(' ')
            outputs.append(wind_method(wa, weatherdict, int(lfields[0]), (lfields[1])))
        elif command.startswith('PRECIPITATION'):
            allfields = command[14:]
            lfields = allfields.split(' ')
            outputs.append(precip_method(wa, weatherdict, int(lfields[0]), (lfields[1])))
    lline = input()
    if lline.startswith('REVERSE NOMINATIM'):
        ra = reversegeocode.ReverseGeocodeAPI(report_location[0], report_location[1])
        new_description = ra.create_description()
    elif lline.startswith('REVERSE FILE'):
        filename = lline[13:]
        p = Path(filename)
        print(p)
        ra = reversegeocode.ReverseGeocodeFile(p)
        new_description = ra.create_desc()
    print(new_description)
    for output in outputs:
        print(str(output[0]) + ' ' + str(output[1]))
    fa.give_credit()
    wa.give_credit()
    ra.give_credit()
    
if __name__ == '__main__':
    run()
    