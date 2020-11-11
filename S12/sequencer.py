"""
Performs a set of instruction to the S12 and returns its results
"""

from os import listdir 
import serial

class Sequencer:
    ser = None             # serial
    output_file = None     # where the output will be printed
    s12_state = None       # state could be 0: S12 ready for macro or 1: S12 ready for command

    def __init__(self):
        """Connects to serial through USB"""
        ser = serial.Serial()
        # parameters
        ser.port = '/dev/ttyS0'
        ser.baudrate =  9600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1 # seconds
        try:
            ser.open()
        except:
            ser.port = '/dev/ttyS1'
            ser.open()
        if ser.isOpen():
            self.ser = ser
            self.ser.write('\x1b'.encode("ascii"))  # get the S12 ready for macro
            self.s12_listen(self)
        else:
            print("Could not connect to either ttys0 nor to ttyS1")
            return None

    def s12_listen(self):
        """
        Listens for the answer of the S12 and returns the S12 state: 
           0: ready for macro 
           1: ready for S12 command
        """
        output_ended = False
        self.s12_state = None
        while not output_ended:
            for line in self.ser.readlines():
                print(line[:-1].decode("ascii"))
                if b">" in line:
                    output_ended = True 
                    self.s12_state = 0
                elif b"<" in line:
                    output_ended = True 
                    self.s12_state = 1

    def exec_command(self, command):
        command += '\r\n'
        if self.s12_state == 0:
            get_ready_for_command(self)
        self.ser.write(command.encode('ascii'))

    def get_ready_for_command(self):
        if self.s12_state != 1:
            while self.s12_state == 0:  # ready for macro
                ser.write('MM\r\n'.encode('ascii'))

