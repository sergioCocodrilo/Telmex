"""
Performs a set of instruction to the S12 and returns its results
"""

from os import listdir 
import serial


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
    """
    Listens for the answer of the S12 and returns the S12 state: 
       0: ready for macro 
       1: ready for S12 command
    """
    output_ended = False
    s12_state = None
    with open("data/output/pares_libres.txt", "a+") as out_f:
        while not output_ended:
            for line in ser.readlines():
                print(line[:-1].decode("ascii"))
                if b">" in line:
                    output_ended = True 
                    s12_state = 0
                elif b"<" in line:
                    output_ended = True 
                    s12_state = 1
                elif b"NOTASS" in line:
                    out_f.write(line[:-1].decode("ascii") + "\n")
    return (s12_state)

def consultar_tablilla(nums):
    # Query the S12
    ser.write('\x1b'.encode("ascii"))

    while s12_listen(ser) == 0:
        ser.write('MM\r\n'.encode('ascii'))

    for num in nums:
        ser.write(("157:GDN=K'" + num + '.\r\n').encode('ascii'))
        while True:
            state = s12_listen(ser)
            if state == 1:
                break
            else:
                ser.write('MM\r\n'.encode('ascii'))

if __name__ == "__main__":
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()

    tablillas = estado_de_tablillas_por_archivo()
    consultar_tablilla(tablillas)
