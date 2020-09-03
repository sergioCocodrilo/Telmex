

from os import listdir 
import serial
import re
import s12_commands

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
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            if b">" in line:
                output_ended = True 
                s12_state = 0
            elif b"<" in line:
                output_ended = True 
                s12_state = 1
    return (s12_state)

def read_data_from_file():
    # Get the list files. They should be in the data/input directory
    files = listdir('data/input/')
    print('Selecciona tu archivo, debe estar en la carpeta data/input/')
    [print('\t', index + 1, ':', f) for index, f in enumerate(files)]
    f = files[int(input('\t Archivo: ')) - 1]
    print('Archivo seleccionado:', f)

    # Get the list of modules to check
    data = []
    with open('data/input/' + f, 'r') as in_file:
        for l in in_file:
            data.append(l[:-1].split())
    return data

def s12_command(ser, command):
    ser.write((command + '\r\n').enocde('ascii'))

def consultar_tablilla(tablillas):
    # Query the S12
    ser.write('\x1b'.encode("ascii"))

    while s12_listen(ser) == 0:
        ser.write('MM\r\n'.encode('ascii'))

    for tablilla in tablillas:
        ser.write(("157:EN=H'" + tablilla + '.\r\n').encode('ascii'))
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

    data = read_data_from_file()[1:]
    commands = [s12_commands.create_single_subscriber(d[0], d[1], d[2]) for d in data]

    ser.write('\x1b'.encode("ascii"))

    for command in commands:
        ser.write('MM\r\n'.encode('ascii'))
        s12_listen(ser)
        ser.write(command[0].encode('ascii'))
        s12_listen(ser)
        #print(command[0])
