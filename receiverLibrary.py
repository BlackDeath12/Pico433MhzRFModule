from machine import Pin
import time
import _thread

class Receiver:
    
    record_time = 150000 #in microseconds
    pin_number = None
    captured_code = ""
    recordInput = [[],[]]
    expectedCodes = []
    code_length = 8
    long_pause = 2000
    short_pause = 800
    upper_bound = 250
    lower_bound = 100
    
    found_code_var = []
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
            
        arr = self.recordInput.copy()
        self.get_input(arr[0], arr[1])
        
    def get_input(self, arr1, arr2):
        first = -1
        second = -1
        for i in range(len(arr1)):
        
            if first == -1:
                if arr2[i] == 0:
                    first = i
                
            else:
                if arr2[i] == 1 and arr2[i - 1] == 0:
                    second = i
                
            if first != -1 and second != -1:
                x = arr1[second] - arr1[first]
    
                if x <= self.short_pause + self.upper_bound and x >= self.short_pause - self.lower_bound:
                    self.captured_code += "1"
                
                elif x <= self.long_pause + self.upper_bound and x >= self.long_pause - self.lower_bound:
                    self.captured_code += "0"
            
                first = -1
                second = -1
                
        if len(arr1) > 0:     
            print(self.captured_code)
        
        if len(arr1) > 0:
            read_message = ""
            for i in range(0, len(self.captured_code) - self.code_length):
                
                for j in range(i, i + self.code_length):
                    read_message += self.captured_code[j]
                
                if len(read_message) == self.code_length:
                    
                    for l in range(len(self.expectedCodes)):
                        if read_message == self.expectedCodes[l]:
                            print('Code at Index:', l, 'Found!')
                            self.found_code(l)
                            read_message = ""
                            
                    read_message = ""
    def print_expected(self):
        
        length = len(self.expectedCodes)
        for i in range(length):
            print("#", i, "code:", self.expectedCodes[i])
        
    def found_code(self, index):
        
            self.found_code_var.append(index)
            
    def get_code(self):
        
        if len(self.found_code_var) > 0:
        
            return self.expectedCodes[self.found_code_var.pop(0)]
        
    def get_index(self):
        
        if len(self.found_code_var) > 0:
            
            return self.found_code_var.pop(0)
    
    def add_expected(self, code):
        
        self.expectedCodes.append(code)
    
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
    
   


