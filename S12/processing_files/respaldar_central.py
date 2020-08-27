'''
Weekly automatic backup.
Restrictions:
    The disk must be already mounted.
'''
import datetime
def backup_commands():
    """
    Weekly system backup
    """

    commands = []
    # build identifier idf
    date = datetime.datetime.now() 
    month = str(date.month) if date.month > 9 else "0"+ str(date.month)
    day = str(date.day) if date.day > 9 else "0"+ str(date.day)
    idf = "AB" + month + day

    # mount disk
    #commands.append('8339:LDEV=DKB2,VOLID="ABASTOS".')
    # write permission

    # select disk 
    # on even weeks the backup is done on disk C
    # on odd weeks on disk D
    d = ("4020", "4021") if datetime.date.today().isocalendar()[1] % 2 == 0 else ("4120", "4121")

    # remove disk protection
    commands.append('8334:LDEV=' + d[0] + ',PROTECT=OFF.')
    commands.append('8334:LDEV=' + d[1] + ',PROTECT=OFF.')

    # start backup
    commands.append('8331:2=Y,5=1032,7=' + d[0] + ',8="' + idf + '",9=' + d[1] + ',10="' + idf + '",11,13=15.')
    return commands

if __name__ == "__main__":
    [print(c) for c in backup_commands()]
