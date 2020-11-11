

# Programa para generar un reporte estadistico de los PBX obtenido por la macro del S12

''' 
1. get_input_file: Ask the user for a file to process
2. read_input_file: Read the input file
    2.1 idenfity all the pbx head numbers of interest
    2.2 make a list out of all the pbx numbers
3. get_pbx_info: get a report for a head number
    3.1 within the report, identify all the associated numbers
    3.2 return a dataframe with its data
4. repeat for each number on the list of 2.2 and produce a report (csv)
'''

def get_input_file():
    input_file = input("Give me the file to process and its location: ")
    try:
        f = open(input_file, 'r')
    except:
        print("File not found")
        exit()
    return f

def read_input_file(f):
    ddi_pbx = []
    no_ddi_pbx = []
    '''
    for l in f:
        if l[49:56].startswith("NO"):
            print(l[10:25].replace(' ',''))
    '''
    [ddi_pbx.append(l[10:25].replace(' ', '')) if l[49:56].startswith('NO') else no_ddi_pbx.append(l[10:25].replace(' ', '')) for l in f]
    print('ddi_pbx:', len(ddi_pbx), '\n no_ddi_pbx:', len(no_ddi_pbx))
    return no_ddi_pbx

import pandas as pd
def get_pbx_info(pbx):
    pass




if __name__ == "__main__":
    f = get_input_file()
    no_ddi_pbx = read_input_file(f)
    example_number = '5556002720'
    get_pbx_info(example_number)

