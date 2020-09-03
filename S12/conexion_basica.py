"""
Raw connection to S12. Just like Hycon.
"""
import serial
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def connect():
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
        return ser
    else:
        return None

def s12_listen(ser):
    """Listens for the answer of the S12 and returns the result"""
    output_ended = False
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            if b"<" in line or b">" in line:
                output_ended = True 

def main():
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()
    print('========== Presiona Ctrl + C para salir ==========')
    ser.write('\x1b'.encode("ascii"))
    while True:
        s12_listen(ser)
        usr_input = input()
        ser.write((usr_input.upper() + '\r\n').encode("ascii"))
    
if __name__ == "__main__":
    main()
