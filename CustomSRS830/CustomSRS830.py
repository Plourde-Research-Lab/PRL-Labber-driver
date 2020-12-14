#!/usr/bin/env python

from VISA_Driver import VISA_Driver

class Driver(VISA_Driver):
    """ The SRS 844 driver re-implements the VISA driver with extra options"""

#    def performOpen(self, options={}):
#        """Perform the operation of opening the instrument connection"""
#        # calling the generic VISA open to make sure we have a connection
#        VISA_Driver.performOpen(self, options=options)
#        # set termination character
#        self.com.term_chars = '\r'

    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        # perform special getValue for reading complex value
        name = str(quant.name)
        if name == 'Value':
            # get complex value in one instrument reading
            sCmd = 'SNAP?1,2'
            sAns = self.askAndLog(sCmd).strip()
            lData =  sAns.split(',')
            # return complex values
            return complex(float(lData[0].strip()), float(lData[1].strip()))
        elif name == 'R':
            #convert resistance to Kelvin
            R_volt = VISA_Driver.performGetValue(self, quant, options=options)
            Amp = 0.01 # 0.01 V
            R_std = 10e6 # standard resistance in Ohm
            R1 = R_volt / (Amp / R_std)  # R: resistance of thermometer
            if R1 > 3590:
                Temp = 377*((1/(R1-1500))+8.22e-6)**0.86296
            else:
                    Temp = 4031*((1/(R1-997.7))+4.54e-5)**1.15512
            return Temp
        else:
            # run the generic visa driver case
            return VISA_Driver.performGetValue(self, quant, options=options)


if __name__ == '__main__':
    pass
