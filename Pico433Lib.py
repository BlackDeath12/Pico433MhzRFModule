from machine import Pin
import time

class Rx:

    long_delay = 500 #Half of the duration of the data transmission period.
    short_delay = int(long_delay/2) #Time in microseconds. A quarter of the duration of the data transmission period.
    
    package_size = 10 #Size of the package in bytes (excluding header size and size flag).
    
    data_set = 0
    data = [[]]
    max_storage = 5
    
    def __init__(self, pin_number, protocol, header):

        self.rx_pin = Pin(pin_number, Pin.IN, Pin.PULL_DOWN)
        self.protocol = protocol
        self.header = header

        print('Receiver set at:', self.rx_pin)

        print('Expected package header:', header)
        self.checkBit = protocol ^ 1
        print("Waiting for signal to transition to", str(self.checkBit) + "...")
   
    def listen(self):
        
        num_bits = 0
        byte = 0
        self.num_bytes = 0
        header_bits = 0
        header_done = False
        size_flag_done = False
        self.errors = False

        while (not self.errors) and (self.num_bytes < self.package_size):
            
            while self.rx_pin.value() == self.checkBit:

                time.sleep_us(self.short_delay)
                
                if self.rx_pin.value() != self.checkBit:
                    self.errors = True
                    self.data[self.data_set].clear()
                    
                    if header_done and self.num_bytes != self.package_size:
                        print("\n``````````````````````")
                        print("Transmission Error!")
                        print("Bytes received:", self.num_bytes)
                        print("Expected package size:", self.package_size)
                        print("``````````````````````")
                    
                
                else:
                    
                    self.current_bit = self.checkBit ^ self.protocol

                    time.sleep_us(self.long_delay)

                    if self.rx_pin.value() == self.checkBit:
                        
                        self.checkBit = self.checkBit ^ 1
                    
                    #Measure processing time
                    #timeOne = time.ticks_us()
                    
                    num_bits += 1
                    
                    byte = byte << 1
                    
                    byte = byte | self.current_bit
                    
                    if (not header_done) and self.header[header_bits] == self.current_bit:
                        
                        header_bits += 1
                        
                        if header_bits == len(self.header):
 
                            header_done = True
                            
                            num_bits = 0
                            
                            byte = 0
                            
                    elif header_done:
                        
                        if (not size_flag_done):
                            
                            if num_bits == 8:
                                
                                self.package_size = byte
                                
                                byte = 0
                                
                                num_bits = 0
                                
                                size_flag_done = True
                                
                        else:
                            
                            if num_bits == 8:
                                
                                print(chr(byte), end='')
                                
                                self.__store_byte(byte)
                                
                                self.num_bytes += 1
                                
                                byte = 0
                                
                                num_bits = 0
                                
                                if self.num_bytes == self.package_size:
                                    
                                    self.__package_completed()
                                    
                    
                    else:
                        
                        self.errors = True
                        self.data[self.data_set].clear()
                        
                        if header_done and self.num_bytes != self.package_size:
                            print("\n``````````````````````")
                            print("Transmission Error!")
                            print("Bytes received:", self.num_bytes)
                            print("Expected package size:", self.package_size)
                            print("``````````````````````")
                        
                    #Measure processing time
                    #timeTwo = time.ticks_us()
                    #totalTime = time.ticks_diff(timeTwo, timeOne)
                    #print(totalTime)
        
    def __package_completed(self):
        
        if len(self.data) < self.max_storage + 1:
            
            self.data.append([])
            self.data_set += 1
            
        else:
            
            self.data.pop(0)
            self.data.append([])
    
    def __store_byte(self, byte):
        
        self.data[self.data_set].append(byte)
        
    def get_latest(self):
        
        hexStr = ""
        index = self.data_set - 1
            
        for i in range(len(self.data[index])):
            
            hexStr += hex(self.data[index][i])
            hexStr += ":"
            
        return hexStr
    
    def set_bit_time(self, time):
        
        self.long_delay = int(time/2)
        self.short_delay = int(time/4)
        
    def set_max_storage(self, size):
        
        self.max_storage = size
    
    
class Tx:
    
    long_delay = 500 #in microseconds
    
    def __init__(self, pin, protocol, header):
        
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(protocol)
        
        self.protocol = protocol
        
        self.header = header
        
        print("Transceiver set at:", self.pin)
        
        print("Protocol set at:", protocol)
        
        print("Header to be sent:", header)
    
    def to_bits(self, string):
        bits = ""
        for i in string:
            bits2 = ''.join('{:08b}'.format(ord(j)) for j in i)
            bits += bits2
        return bits
    
    def send_bit(self, bit):
        
        if self.protocol == 0:
            
            if bit == 1 or bit == '1':
                time.sleep_us(self.long_delay)
                self.pin.value(1)
                
                time.sleep_us(self.long_delay)
                self.pin.value(0)
            
            else:
                self.pin.value(1)
                time.sleep_us(self.long_delay)
                
                self.pin.value(0)
                time.sleep_us(self.long_delay)
            
        
        else:
            
            if bit == 1 or bit == '1':
                self.pin.value(1)
                time.sleep_us(self.long_delay)
                
                self.pin.value(0)
                time.sleep_us(self.long_delay)
            
            else:
                time.sleep_us(self.long_delay)
                self.pin.value(1)
                
                time.sleep_us(self.long_delay)
                self.pin.value(0)

        
    def send_message(self, message):
        
        sending = True
        
        while sending == True:
        
            if len(message) > 255:
                
                short_message = message[:255]
                message = message[255:]
                
            else:
                
                short_message = message
                sending = False
            
            size_flag = '{:08b}'.format(len(short_message))
            
            short_message = self.to_bits(short_message)
            
            for i in range(len(self.header)):
               self.send_bit(self.header[i])
               
            for i in range(len(size_flag)):
                self.send_bit(size_flag[i])
                
            for i in range(len(short_message)):
                self.send_bit(short_message[i])
            
            time.sleep(1/8)
            
    def set_bit_time(self, time):
        self.long_delay = time
