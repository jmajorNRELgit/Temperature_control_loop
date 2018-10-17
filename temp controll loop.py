import Sorensen_power_supply_class as power
import Keysight_DAQ_VISA_class as DAQ
import sys
import copy
import numpy as np
from time import sleep

DAQ = DAQ.DAQ('GPIB3::3::INSTR')
print(DAQ.check_for_thermocouples())
channel = [2]

power = power.sorensen_power('GPIB2::1::INSTR')
power.set_current(0)
power.set_voltage(0)

if input('Are you ready to start? y/n: ') == 'n':
    sys.exit()

#start_current = float(input('What current level? ')) or .6
#current = copy.deepcopy(start_current)

power.set_voltage(35)


set_point = 20
for i in np.arange(.7, 1.9, 0.1):
    start_current = i
    current = copy.deepcopy(start_current)
    temp_curve = []
    
    for i in range(500):
        sleep(.5)
        #protection
        if current > 2:
            print('over current')
            break
    #take temp and find the difference between current temp and setpoint
        temp = DAQ.measure_thermocouples(channel)
        temp_curve.append(temp)
        diff = set_point - temp[0]
        print(temp)
        
        if diff > 10:
            power.set_current(current)
            if len(temp_curve) % 10 == 0:
                if np.std(temp_curve[-5:]) < 2:
                    current = current + .1
                    print('+ .1')
        
        elif diff  < 10 and diff > 5:
            power.set_current(current - .05) 
            if len(temp_curve) % 2 == 0:
                if np.std(temp_curve[-5:]) < 1:
                    current = current + .1
                    print('+ .1')
        
        elif diff <5 and diff > 2.5:
            power.set_current(current - .2)
            if len(temp_curve) % 2 == 0:
                if np.std(temp_curve[-5:]) < .5:
                    current = current + .05
                    print('+ .05')
        
        elif diff <2.5 and diff > 1.5:
            power.set_current(current - .25)
            if len(temp_curve) % 2 == 0:
                if np.std(temp_curve[-5:]) < .5:
                    current = current + .05
                    print('+ .05')
        
        elif diff < .5 and diff > 0:
            top =1
            power.set_current(current - .03)
            
        elif diff < 0 and diff > -5:
            power.set_current(current - .035)
            if len(temp_curve) % 2 == 0:
                current = current - .025
                print('Dropped .05')
            
        elif diff < -1 and diff > -15:
            power.set_current(current - .45)
            if len(temp_curve) % 2 == 0:
                current = current - .1
                print('Dropped .1...')
    
        elif diff < -15:
            power.set_voltage(0)
            power.set_voltage(0)
            power.close()
            print('Overtemp')
            break
        
        
        


#shut power off
power.set_voltage(0)
power.set_voltage(0)
power.close_com()
