# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:04:00 2018

@author: jmajor
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:43:13 2018

@author: jmajor
"""

import visa
import time
import numpy as np

class DAQ():
    
    def __init__(self, com_port):
        self.name = 'HEWLETT-PACKARD,34970A,0,13-2-2\n'
        
        self.com_port = com_port
        
        self.rm = visa.ResourceManager()
        
        self.inst = self.rm.open_resource(self.com_port)
        
        if self.inst.query('*IDN?') == self.name:
            print('Communication established with Keysight DAQ')
            
        else:
            print('Communication FAILED with Keysight DAQ')
            
        self.channels = None
        
    
    def check_for_thermocouples(self):

        #Takes measurements on each of the 20 chanels
        temps = str(self.inst.query('MEAS:TEMP? TCouple, K, (@101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120)'))

        #return temps
        time.sleep(.5)


        #Turns the temperature reading into a list of temps
        temps = list(map(float, temps.rstrip('\n').split(',')))

        temps = np.array(temps)

        #Empty thermocouple chanels read very large negative numbers so this finds where
        #the chanel readings are above -100 degrees
        #Add 1 because the chanels start at 101 and not 100
        thermocuople_locations = np.where(temps > -100)[0] +1

        print('\nThermocouples found on chanels: {0}'.format(str(thermocuople_locations)))

        self.channels = list(thermocuople_locations)
        
        return list(thermocuople_locations)

        
    def measure_thermocouples(self, channels = None):
        #print('Reading temperatures from DAQ')
        if channels == None:
            channels = self.channels
        channel_list = []
        for location in channels:
            if int(location) <10:
                channel_list.append('10{0}'.format(str(location)))
            else:
                channel_list.append('1{0}'.format(str(location)))

        channel_list = str(channel_list).rstrip(']').lstrip('[').replace("'", "")
        
        command = 'MEAS:TEMP? TCouple, K, (@{0})'.format(channel_list)
        temp_list = self.inst.query(command)
        temp_list = temp_list.replace('+','')
        temp_list = temp_list.replace('\n','')
        return list(map(float,temp_list.split(',')))
    
    def close(self):
        self.inst.close()

if __name__ == '__main__':
    daq = DAQ('GPIB3::3::INSTR')
    print(daq.check_for_thermocouples())
    temps = daq.measure_thermocouples()
