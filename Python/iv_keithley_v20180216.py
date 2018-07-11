#!/usr/local/bin python

# Responsivity DAQ routine

import time
from datetime import date
from math import *
from numpy import *
from scipy import io
from scipy import optimize
from visa import *
from matplotlib import pyplot as plt
print "got here0"

#bv1= linspace(-1.5, -0.5, 101)
#bv2= linspace(-0.49, 0, 50)
#bv3= linspace(0.01, 0.25, 25)
#bv4= linspace(0.26, 0.5, 25)

#bva = append(bv1,bv2)
#bvb = append(bv3,bv4)

#bias_voltages = append(bva,bvb)
bias_voltages = linspace(-5, 5, 201)

start_voltage = min(bias_voltages)
end_voltage = max(bias_voltages)

bias_steps = len(bias_voltages)

device_description = "pSi_PD_fixed_7_1220_tap70uW"

timeTuple = time.localtime()
Resp_OutFileName = ".\\iv_%s_%d-%d-%d_%d#%d#%d--%d#%d#%d.mat" % (
                            device_description,
                            start_voltage,
                            bias_steps,
                            end_voltage,
                            timeTuple[0],
                            timeTuple[1],
                            timeTuple[2],
                            timeTuple[3],
                            timeTuple[4],
                            timeTuple[5])

Figure_OutFileName = ".\\iv_%s_%d-%d-%d_%d#%d#%d--%d#%d#%d.png" % (
                            device_description,
                            start_voltage,
                            bias_steps,
                            end_voltage,
                            timeTuple[0],
                            timeTuple[1],
                            timeTuple[2],
                            timeTuple[3],
                            timeTuple[4],
                            timeTuple[5])

sparam = instrument("GPIB::15", timeout = 3)

print "got here2"

# Initialize semiconductor parameter analyzer
sparam.write("*RST")
time.sleep(1.0)
sparam.write(':SOUR:FUNC VOLT')
sparam.write(':SENS:FUNC "CURR"')
sparam.write(':SOUR:SWE:RANG AUTO')
sparam.write(':SENS:CURR:PROT 0.001')
sparam.write(':SENS:CURR:RANG:AUTO 1')
sparam.write(':SENS:CURR:NPLC 1')
sparam.write(':SOUR:VOLT:LEV:AMPL 0.0')

sparam.write(':OUTP ON')


measurements = zeros((bias_steps,2))

row=0
# Enter measurement loop
bias_index = 0
for bias_current in bias_voltages:

    sparam.write(':SOUR:VOLT:LEV:AMPL %.3f' % bias_current)
    print "Setting bias to", bias_current, "V"

    time.sleep(0.01)
        
    measurements[bias_index,0] = bias_current

    sparam.write(":INIT")
            
    time.sleep(0.1)
                            
    # Test    
    current_meas_array = sparam.ask_for_values(":FETC?")

    current_meas = current_meas_array[1]

    print "current", current_meas*1e6, "uA"
    measurements[bias_index,1] = current_meas

    bias_index = bias_index+1


sparam.write(':OUTP OFF')


# Plot
plt.plot(measurements[:,0], measurements[:,1], 'r--')

#plt.xlim([0, 20])
plt.xlabel("Bias Voltage [V]")
plt.ylabel("Diode Current [uA]")

plt.show()
plt.savefig(Figure_OutFileName, dpi=300)


# Save to .mat file
io.savemat(Resp_OutFileName, {'IV_data': measurements})
