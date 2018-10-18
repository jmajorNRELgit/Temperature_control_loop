# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 10:32:51 2018

@author: jmajor
"""

############################################################################################
#
# PID algorithm to take input sensor readings, and target requirements, and
# as a result feedback new rotor speeds.
#
############################################################################################
class PID:

	def __init__(self, p_gain, i_gain, d_gain, now):
		self.last_error = 0.0
		self.last_time = now

		self.p_gain = p_gain
		self.i_gain = i_gain
		self.d_gain = d_gain

		self.i_error = 0.0


	def Compute(self, input, target, now):
		dt = (now - self.last_time)

		#---------------------------------------------------------------------------
		# Error is what the PID alogithm acts upon to derive the output
		#---------------------------------------------------------------------------
		error = target - input

		#---------------------------------------------------------------------------
		# The proportional term takes the distance between current input and target
		# and uses this proportially (based on Kp) to control the ESC pulse width
		#---------------------------------------------------------------------------
		p_error = error

		#---------------------------------------------------------------------------
		# The integral term sums the errors across many compute calls to allow for
		# external factors like wind speed and friction
		#---------------------------------------------------------------------------
		self.i_error += (error + self.last_error) * dt
		i_error = self.i_error

		#---------------------------------------------------------------------------
		# The differential term accounts for the fact that as error approaches 0,
		# the output needs to be reduced proportionally to ensure factors such as
		# momentum do not cause overshoot.
		#---------------------------------------------------------------------------
		d_error = (error - self.last_error) / dt

		#---------------------------------------------------------------------------
		# The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
		#---------------------------------------------------------------------------
		p_output = self.p_gain * p_error
		i_output = self.i_gain * i_error
		d_output = self.d_gain * d_error

		#---------------------------------------------------------------------------
		# Store off last input for the next differential calculation and time for next integral calculation
		#---------------------------------------------------------------------------
		self.last_error = error
		self.last_time = now

		#---------------------------------------------------------------------------
		# Return the output, which has been tuned to be the increment / decrement in ESC PWM
		#---------------------------------------------------------------------------
		return p_output, i_output, d_output






import Keysight_DAQ_VISA_class as DAQ
import Sorensen_power_supply_class as power
from time import time
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import sys

DAQ = DAQ.DAQ('GPIB1::3::INSTR')
print(DAQ.check_for_thermocouples())
channel = [2]

power = power.sorensen_power('GPIB2::1::INSTR')
power.set_current(2)
power.set_voltage(0)

temp_pid = PID(.9, .02, 1, time())

set_point = -30

voltage = sum(temp_pid.Compute(DAQ.measure_thermocouples([2])[0],20,time()))

master_temp = []



for i in np.arange(-30,10,10):
    set_point = i
    while True:
        try:
            temp = DAQ.measure_thermocouples([2])[0]
            voltage = sum(temp_pid.Compute(temp,set_point,time()))
            master_temp.append(temp)
            print('STD: ', np.std(master_temp[-10:]))
            print(voltage)
            power.set_voltage(voltage)
            if temp < set_point +1 and temp > set_point -1 and np.std(master_temp[-10:]) < .05:
                for i in range(30):
                    temp = DAQ.measure_thermocouples([2])[0]
                    master_temp.append(temp)
                    sleep(1)
                print('Next temp')
                break
            sleep(1)


        except:
            power.set_voltage(0)
            print('Error')
            print(max(master_temp))
            plt.plot(master_temp)
            sys.exit()
            break

power.set_voltage(0)
print('Error')
print(max(master_temp))
plt.plot(master_temp)
