# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:43:13 2018

@author: jmajor
"""

import visa

class sorensen_power():
    
    def __init__(self, com_port):
        self.name = 'SORENSEN, DLM60-10M9G, 0128A2029, 1.04, 1.01\r\n'
        
        self.com_port = com_port
        
        self.rm = visa.ResourceManager()
        
        self.inst = self.rm.open_resource(self.com_port)
        
        if self.inst.query('*IDN?') == self.name:
            print('Communication established with Sorensen power supply')
            
        else:
            print('Communication FAILED with Sorensen power supply')
        
    def set_voltage(self, voltage):
        
        self.inst.write('SOUR:volt {}'.format(str(voltage)))
        
    def set_current(self, current):
        
        self.inst.write('SOUR:curr {}'.format(str(current)))
        
    def close_com(self):
        self.inst.close()
        
        