"""
Raw connection to S12. Just like Hycon.
"""
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
    """Listens for the answer of the S12 and returns the result"""
    # logging all outputs
    try:
        log_file = open('data/output/s12_raw.log', 'a')
    except:
        print('Error en la estructura de los archivos, descarga de nuevo el proyecto.')
        print('Para descargarlo: git clone https://github.com/sergioCocodrilo/S12_raw.git')
        quit()
    output_ended = False
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            log_file.write(line.decode('ascii'))
            if b"<" in line or b">" in line:
                output_ended = True 
    log_file.close()
    
if __name__ == "__main__":
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
