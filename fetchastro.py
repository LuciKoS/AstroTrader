import swisseph as swe
import datetime
import numpy as np
import math

def astrosell(n):

    swe.set_ephe_path('/Users/lucbaumeler/documents/eth/vscode/projects/astrotrader/ephe')

    now = datetime.datetime.utcnow()

    ut_time = now.hour + now.minute/60 + now.second/3600
 
    jd = swe.julday(now.year, now.month, now.day, ut_time)
    
    

    ceres_result = swe.calc_ut(jd, swe.CERES)
    ceres_lon_deg = ceres_result[0][0] 

    ceres_offset_fraction = ceres_lon_deg / 360.0

    ceres_offset = 2 * math.pi * ceres_offset_fraction

    seconds_in_day = now.hour * 3600 + now.minute * 60 + now.second
    fraction_of_day = seconds_in_day / 86400.0
    
   
    oscillation_factor = 10 
    phase = (2 * math.pi * fraction_of_day * oscillation_factor) + ceres_offset
    
    
    value = (math.sin(phase) + 1) / 2

    return value


print(astrosell(10))

def astrobuy(n):
    
    swe.set_ephe_path('/Users/lucbaumeler/documents/eth/vscode/projects/astrotrader/ephe')
    
    
    now = datetime.datetime.utcnow()
    
    ut_time = now.hour + now.minute / 60 + now.second / 3600
    
   
    jd = swe.julday(now.year, now.month, now.day, ut_time)
    
   
    jupiter_result = swe.calc_ut(jd, swe.JUPITER)
  
    jupiter_lon_deg = jupiter_result[0][0]
    
   
    jupiter_offset_fraction = jupiter_lon_deg / 360.0
    jupiter_offset = 2 * math.pi * jupiter_offset_fraction

    
    seconds_in_day = now.hour * 3600 + now.minute * 60 + now.second
    fraction_of_day = seconds_in_day / 86400.0

   
    oscillation_factor = 10
    
    phase = (2 * math.pi * fraction_of_day * oscillation_factor) + jupiter_offset

   
    value = (math.sin(phase) + 1) / 2
    return value

print(astrobuy(10))
