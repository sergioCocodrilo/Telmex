


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

if __name__ == "__main__":
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()

    # Get the list files. They should be in the data/input directory
    files = listdir('data/input/')
    print('Selecciona tu archivo, debe estar en la carpeta data/input/ y ser del tipo .csv')
    csv_files = list(filter(lambda f: f.endswith(".csv"), files))
    [print('\t', index + 1, ':', f) for index, f in enumerate(csv_files)]
    f = csv_files[int(input('\t Archivo: ')) - 1]
    print('Archivo seleccionado:', f)

    # Query the S12
    print('\t========== Revisando las troncales ==========')
    ser.write('\x1b'.encode("ascii"))
    while s12_listen(ser)[0] == 0:
        ser.write('MM\r\n'.encode('ascii'))

    # Get the list of modules to check
    df = pd.read_csv('data/input/' + f)
    df["DISPLAY-TRUNK"] = ""
    for index, module in enumerate(df.iloc[:,0]):
        print('Consultando', module)
        ser.write(("DISPLAY-TRUNK:NA1=" + module + ',TSLIST1=1.\r\n').encode('ascii'))
        while True:
            state, comment = s12_listen(ser)
            if comment != "":
                df.iloc[index,-1] = comment
            if state == 1:
                break
            else:
                ser.write('MM\r\n'.encode('ascii'))

    df.to_csv("data/output/" + f, index=False)
    print('\t========== Resultado guardado en data/output ==========')

