"""Connects to serial through Serial Port"""

import serial

class S12Connection:
    def __init__(self):
        self.ser = serial.Serial()
        # parameters
        self.ser.port = '/dev/ttyS0'
        self.ser.baudrate =  9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1 # seconds
        try:
            self.ser.open()
        except:
            self.ser.port = '/dev/ttyS1'
            self.ser.open()
        if self.ser.isOpen():
            self.status = "connected"
        else:
            self.status = "disconnected"

    def execute_command(self, commands):
        """Send commands to server, commands should be an input list"""
        for command in commands:
            self.ser.write('\x1b'.encode("ascii"))
            self.listen()
            self.ser.write(b"MM\r\n")
            self.listen()
            self.ser.write(command.encode("ascii") + b"\r\n")
            response = self.listen()
            """ AGREGAR UN BREAK SI LA PRIMERA INSTRUCCIÓN FALLA.
            NO TIENE SENTIDO TRATAR DE EJECUTAR LA SIGUIENTE,
            TAMBIÉN FALLARÁ PERO EL SISTEMA NO RESONDE."""

    def listen(self, verbose = True):
        """Listens for the answer of the S12 and returns the result"""
        output_ended = False
        server_response = []
        while not output_ended:
            new_lines = self.ser.readlines()
            server_response.extend(new_lines)
            for line in new_lines:
                if verbose:
                    print(line.decode("ascii"))
                if b"<" in line or b">" in line:
                    output_ended = True 
        return server_response
