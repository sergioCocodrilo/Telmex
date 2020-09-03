"""Builds the text for making native S12 commands"""


# built in, single functions

def nums_en_mod(na):
    return ["157:EN=H'" + na + "."]

def create_single_subscriber(dn, na, lan,):
    return ["5289:2=K'" + dn + ",6=H'" + na + ",8=" + lan + ''',106="SUBG02",46=1,45=1&K'01&K'123&1&K'00&K'123.''']

def remove_single_subscriber(dn):
    return ["5292:DN=K'" + dn + "."]

def display_any_subscriber(dn):
    return ["5297:DN=K'" + dn + "."]


# pipe of commands

def new_module(dn, na, lan):
    commands = remove_single_subscriber(dn)
    commands.extend(create_single_subscriber(dn, na, lan))
    return commands

import datetime
def start_backup():
    """Weekly system backup"""
    date = datetime.datetime.now() # build identifier idf
    month = str(date.month) if date.month > 9 else "0"+ str(date.month)
    day = str(date.day) if date.day > 9 else "0"+ str(date.day)
    idf = "AB" + month + day
    # mount disk
    commands.append('8339:LDEV=DKB2,VOLID="ABASTOS".')
    # write permission
    commands.append('8334:LDEV=4120,PROTECT=OFF.')
    commands.append('8334:LDEV=4121,PROTECT=OFF.')
    # backup
    commands.append('8331:2=Y,5=1032,7=4120,8="' + idf + '",9=4121,10="' + idf + '",11,13=15.')
    return commands

def change_multiple_modules():
    commands = []
    with open("data/input/cambio_de_dispositivo", "r") as f:
        next(f)
        try:
            for line in f:
                dn, na, lan = line.split()
                commands.extend(new_module(dn, na, lan))
        except:
            raise ValueError("Error en el archivo cambio_de_dispositivo")
    return commands

def translate_sblrit(source_file):
    commands = []
    with open("Input_lists/" + source_file, 'r') as f:
        for l in f:
            commands.append('39:9=1,4=CTLE,NA=' + l + ',NBR=1.')
    return commands
   
