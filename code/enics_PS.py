from PyMCP2221A import PyMCP2221A
import time

class run_class:
    def init_PS(self):
        self.mcp2221 = PyMCP2221A.PyMCP2221A()
        self.mcp2221.Reset()
        self.mcp2221 = PyMCP2221A.PyMCP2221A()
        self.mcp2221.I2C_Init()
        
        #Mux address select - Page 5 bottom, pca9548a.pdf - U3 A0 is at 5V and U1 A0 is at GND
        #Channel select - Page 16-17, pca9548a.pdf - channels 0,2,4,6 are LDO potentiometers
        self.ldo_mux_and_channel = { 0 : [0x71, 0x20],      #U3, ch6 = 0b01000000
                                     1 : [0x71, 0x10],      #U3, ch4 = 0b00010000
                                     2 : [0x71, 0x4 ],      #U3, ch2 = 0b00000100
                                     3 : [0x71, 0x1 ],      #U3, ch0 = 0b00000001
                                     4 : [0x70, 0x20],      #U1, ch6 = 0b01000000 
                                     5 : [0x70, 0x10],      #U1, ch4 = 0b00010000
                                     6 : [0x70, 0x4 ],      #U1, ch2 = 0b00000100
                                     7 : [0x70, 0x1 ] }     #U1, ch0 = 0b00000001
        
        #Mux address select - Page 5 bottom, pca9548a.pdf - U3 A0 is at 5V and U1 A0 is at GND
        #Channel select - Page 16-17, pca9548a.pdf - channels 1,3,5,7 are current limit potentiometers
        self.current_mux_and_channel = { 0 : [0x71, 0x40],  #U3, ch7 = 0b10000000 
                                         1 : [0x71, 0x20],  #U3, ch5 = 0b00100000
                                         2 : [0x71, 0x8 ],  #U3, ch3 = 0b00001000
                                         3 : [0x71, 0x2 ],  #U3, ch1 = 0b00000010
                                         4 : [0x70, 0x40],  #U1, ch7 = 0b10000000 
                                         5 : [0x70, 0x20],  #U1, ch5 = 0b00100000
                                         6 : [0x70, 0x8 ],  #U1, ch3 = 0b00001000
                                         7 : [0x70, 0x2 ] } #U1, ch1 = 0b00000010
                                             
    def write_to_potentiometer(self, mux, channel, val):
        if val > 0x7F or val < 0:
            exit("Error: illegal potentiometr value - " + str(val))
    
        # select channel
        data=[0]*1
        data[0] = channel #turn on the channel to be accessed trough 0x2E address
        self.mcp2221.I2C_Write(mux, data)

        # write to potentiometer trough the openned channel
        data=[0]*2
        data[0] = 0x00  #command to whipe register
        data[1] = val   #any number - what we write to potentiometer (0x00 - 0x7F) 
        self.mcp2221.I2C_Write(0x2E,data)
        
    def read_from_potentiometer(self, mux, channel):
        # select channel
        data=[0]*1
        data[0] = channel  #turn on 0x2E - to connect to slave address of potentiometer 
        # all the potentiometers have same address so we need expanders to connect them on different channels
        self.mcp2221.I2C_Write(mux, data)
        rdata = self.mcp2221.I2C_Read(0x2E,1)  #read from potentiomer 
        return rdata

    def write_val_to_ldo(self, ldo, val):
        mux = self.ldo_mux_and_channel[ldo][0]
        channel = self.ldo_mux_and_channel[ldo][1]
        self.write_to_potentiometer(mux, channel, val)
                
    def write_val_to_current_lim(self, ldo, val):
        mux = self.current_mux_and_channel[ldo][0]
        channel = self.current_mux_and_channel[ldo][1]
        self.write_to_potentiometer(mux, channel, val)    
            
    def read_val_from_ldo(self, ldo):
        mux = self.ldo_mux_and_channel[ldo][0]
        channel = self.ldo_mux_and_channel[ldo][1]
        return self.read_from_potentiometer(mux, channel)
        
    def read_val_from_cur_lim(self, ldo):
        mux = self.current_mux_and_channel[ldo][0]
        channel = self.current_mux_and_channel[ldo][1]
        return self.read_from_potentiometer(mux, channel)

    def set_approx_mV(self, ldo, mV):
        val = int(mV / ( 4750 / 0x80 ))
        self.write_val_to_ldo(ldo, val)
        
       
     
def test_ldos_numbers():
    a=run_class()
    a.init_PS()
    a.write_val_to_ldo(ldo=0, val=0x00)
    rdata = a.read_val_from_ldo(ldo=0)
    print(rdata)
    a.write_val_to_ldo(ldo=1, val=0x10)
    rdata = a.read_val_from_ldo(ldo=1)
    print(rdata)
    a.write_val_to_ldo(ldo=2, val=0x20)
    rdata = a.read_val_from_ldo(ldo=2)
    print(rdata)
    a.write_val_to_ldo(ldo=3, val=0x30)
    rdata = a.read_val_from_ldo(ldo=3)
    print(rdata)
    a.write_val_to_ldo(ldo=4, val=0x40)
    rdata = a.read_val_from_ldo(ldo=4)
    print(rdata)
    a.write_val_to_ldo(ldo=5, val=0x50)
    rdata = a.read_val_from_ldo(ldo=5)
    print(rdata)
    a.write_val_to_ldo(ldo=6, val=0x60)
    rdata = a.read_val_from_ldo(ldo=6)
    print(rdata)
    a.write_val_to_ldo(ldo=7, val=0x70)
    rdata = a.read_val_from_ldo(ldo=7)
    print(rdata)


if __name__=="__main__":
    #test_ldos_numbers()
    a=run_class()
    a.init_PS()
    a.set_approx_mV(ldo=5, mV=2750)
