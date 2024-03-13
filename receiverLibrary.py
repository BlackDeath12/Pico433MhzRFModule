from machine import Pin
import time

class Receiver:
    
    record_time = 150000 #in microseconds
    pin_number = None
    captured_code = ""
    recordInput = [[],[]]
    expectedCodes = []
    code_length = 8
    long_pause = 1000
    short_pause = 500
    upper_bound = 100
    lower_bound = 100
    
    found_code_var = -1
    is_new_code = False
    
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_DOWN)
        self.pin_number = pin_number
        
    def get_value(self):
        return self.pin.value()
    
    def set_pause_length(self, short_pause, long_pause):
        self.long_pause = long_pause
        self.short_pause = short_pause
    
    def listen(self):
        
        self.recordInput = [[],[]]
        self.captured_code = ""
        
        total_time = 0
        start_time = time.ticks_us()
        
        #===STARTED RECORDING===
        
        while total_time < self.record_time:
            
            time_change = time.ticks_diff(time.ticks_us(), start_time)
            self.recordInput[0].append(time_change)
            self.recordInput[1].append(self.get_value())
            total_time = time_change

        #===ENDED RECORDING===
            
        first = 0
        second = 0
        for i in range(len(self.recordInput[0])):
        
            if first == 0:
                if self.recordInput[1][i] == 1:
                    first = i
                
            elif first != 0:
                if self.recordInput[1][i] == 1:
                    second = i
                
            if first != 0 and second != 0:
                x = self.recordInput[0][second] - self.recordInput[0][first]
    
                if x <= self.short_pause + self.upper_bound and x >= self.short_pause - self.lower_bound:
                    self.captured_code += "1"
                
                elif x <= self.long_pause + self.upper_bound and x >= self.long_pause - self.lower_bound:
                    self.captured_code += "0"
            
                first = second
                second = 0
                
        if len(self.recordInput[0]) > 0:     
            print(self.captured_code)
        
        if len(self.recordInput[0]) > 0:
            read_message = ""
            for i in range(0, len(self.captured_code) - self.code_length):
                
                for j in range(i, i + self.code_length):
                    read_message += self.captured_code[j]
               
                if len(read_message) == self.code_length:
                    
                    for j in range(len(self.expectedCodes)):
                        if read_message == self.expectedCodes[j]:
                            print('Code Found at index:', j)
                            self.found_code(j)
                            break
                        read_message = ""
                    
    def print_expected(self):
        
        length = len(expectedCodes)
        for i in range(length):
            print("#", i, "code:", expectedCodes[i])
        
    def found_code(self, index):
        
            self.is_new_code = True
            self.found_code_var = index
            
    def get_code(self):
            
        return self.expectedCodes[self.found_code_var]
    
    def add_expected(self, code):
        
        new_expected = ''
        new_expected = code
            
        self.expectedCodes.append(new_expected)
    
    def delete_expected(self):
        
        self.expetedCodes.clear()
    
    def set_code_length(self, length):
        self.code_length = length
    
    def set_long_pause(self, long):
        self.long_pause = long
        
    def set_short_pause(self, short):
        self.short_pause = short
        
    def get_long_pause(self):
        return self.long_pause
    
    def get_short_pause(self):
        return self.short_pause
    
    def get_code_legnth(self):
        return self.code_length
    
    def get_record_time(self):
        return self.record_time
    
    def set_record_time(self, time):
        self.record_time = time
    
   

