"""
Most common commands of S12
"""

import serial
import s12_commands as s12

def connect():
    """Connects to serial through SERIAL"""
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

def show_menu():
    """Shows menu and reads input"""
    choice = -1
    while choice not in range(0,10):
        print("""

        Selecciona una instrucción:

            0. Salir

            1. Consulta de dispositivo
            2. Cambio de dispositivo
            3. Alta
            4. Baja

            5. Backup
            6. Resumen de todos los números
            7. Números en un módulo

            8. Cambio de varos dispositivos

            9. Imprimir ubicaciones de módulos
            
        """)
        usr_input = ask_user_for_input("Instrucción")
        if usr_input.isdigit():
            choice = int(usr_input)
    return choice

def ask_user_for_input(msg):
    return input("{:>40}: ".format(msg))

def s12_listen(ser):
    """Listens for the answer of the S12 and returns the result"""
    output_ended = False
    server_response = []
    while not output_ended:
        server_response.extend(ser.readlines())
        for line in server_response:
            if b"<" in line or b">" in line:
                output_ended = True 
    return server_response
    
def build_command(choice):
    """Builds the insctruction text"""
    # get input parameters from user
    if choice in [1,2,3,4]:
        dn = ask_user_for_input("Número")
    if choice in [2,3,7]:
        na = ask_user_for_input("Módulo")
    if choice in [2,3]:
        lan = ask_user_for_input("Par")
    if choice in [8]:
        _ = ask_user_for_input("Los datos se tomarán de cambio_de_dispositivo")
    if choice in [9]:
        source_file = ask_user_for_input("Archivo con la lista de módulos")
    
    commands = None
    if choice == 1:    # consulta de dispositivo
        commands = s12.display_any_subscriber(dn)
    elif choice == 2:  # cambio de dispositivo
        commands = s12.new_module(dn, na, lan)
    elif choice == 3:  # alta de número
        commands = s12.create_single_subscriber(dn, na, lan)
    elif choice == 4:  # baja de número
        commands = s12.remove_single_subscriber(dn)
    elif choice == 5:  # backup
        commands = s12.start_backup()
    elif choice == 6:  # resumen todos nums
        pass
    elif choice == 7: # números en un módulo
        commands = s12.nums_en_mod(na)
    elif choice == 8: # cambio de varios dispositivos
        commands = s12.change_multiple_modules()
    elif choice == 9:
        commands = s12.translate_sblrit(source_file)
        
    return commands

def execute_command(ser, commands, choice):
    """Send commands to server"""
    for command in commands:
        ser.write('\x1b'.encode("ascii"))
        s12_listen(ser)
        ser.write(b"MM\r\n")
        s12_listen(ser)
        ser.write(command.encode("ascii") + b"\r\n")
        response = s12_listen(ser)
        [print(line[:-1].decode("ascii")) for line in response]
        """ AGREGAR UN BREAK SI LA PRIMERA INSTRUCCIÓN FALLA.
        NO TIENE SENTIDO TRATAR DE EJECUTAR LA SIGUIENTE,
        TAMBIÉN FALLARÁ PERO EL SISTEMA NO RESONDE."""

def display_menu():
    """Shows the functions of the S12"""
    ser = connect()
    while 1:
        choice = show_menu()
        if choice == 0:
            break
        commands = build_command(choice)
        if commands:
            execute_command(ser, commands, choice)
    ser.close()

if __name__ == "__main__":
    display_menu()
