from infosys import infosys

infosysKey = '2b62ff22-a815-42e3-9e71-c8480ffbf3fd' #this key requires 2 spaces

def setup():
    global infosysKey
    info = infosys(infosysKey)
    info.addText(0, 'TO CSH! <PICTUREFILE:1>', 'WELCOME')
    info.addPicture(1, ['2222226', '2111026', '2100626', '2111666', '2001626', '2111026', '2222226'])

if __name__ == '__main__':
    setup()
