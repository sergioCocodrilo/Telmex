
from os import listdir 
import serial
import re
import pandas as pd

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
    comment = ""
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            if b">" in line:
                output_ended = True 
                s12_state = 0
            elif b"<" in line:
                output_ended = True 
                s12_state = 1
            elif b"COMMENT" in line:
                comment = line[16:-2].decode("ascii")
    return (s12_state, comment)

def estado_de_tablillas_por_archivo():
    # Get the list files. They should be in the data/input directory
    files = listdir('data/input/')
    print('Selecciona tu archivo, debe estar en la carpeta data/input/ y ser del tipo')
    [print('\t', index + 1, ':', f) for index, f in enumerate(files)]
    f = csv_files[int(input('\t Archivo: ')) - 1]
    print('Archivo seleccionado:', f)

    # Get the list of modules to check
    modules_to_check = []
    with open('data/input/' + f, 'r') as in_file:
        for l in in_file:
            if l.startswith("H'"):
                modules_to_check.append(l[2:6])

def estado_de_todas_las_tablillas():
    pass

def consultar_tablilla(tablillas):
    # Query the S12
    ser.write('\x1b'.encode("ascii"))

    while s12_listen(ser)[0] == 0:
        ser.write('MM\r\n'.encode('ascii'))

    for tablilla in tablillas:
        ser.write(("157:EN=H'" + tablilla + '.\r\n').encode('ascii'))
        while True:
            state, comment = s12_listen(ser)
            '''
            if comment != "":
                module_state.append((module, comment))
            '''
            if state == 1:
                break
            else:
                ser.write('MM\r\n'.encode('ascii'))


if __name__ == "__main__":
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()

    print("Selecciona una opción:")
    print("\t1. Revisar tablillas indicadas en un archivo")
    print("\t2. Revisar todas las tablillas")
    print("\n\t0. Salir")

    user_choice = None
    while user_choice not in [0, 1, 2]:
        user_choice = int(input("\tOpción"))

    if user_choice == 0:
        quit()
    elif user_choice == 1:
        estado_de_tablillas_por_archivo()
    else:
        estado_de_todas_las_tablillas()
