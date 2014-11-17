

class command():

    ''' CONSTANTS'''

    #What you want the sign to do
    COMMAND_CODES = { 'WRITE TEXT': "A",
        'READ TEXT': "B",
        'WRITE SPECIAL': "E",
        'READ SPECIAL': "F",
        'WRITE STRING': "G",
        'READ STRING': "H",
        'WRITE SMALL DOTS': "I",
        'READ SMALL DOTS': "J",
        'WRITE RGB DOTS': "K",
        'READ RGB DOTS': "L",
        'WRITE LARGE DOTS': "M",
        'READ LARGE DOTS': "N",
        'WRITE ALPHAVISION': "O",
        'SET TIMEOUT': "T" }

    #Special functions.. I guess
    SPECIAL_FUNCTIONS = { 'SET TIME': "\x20",
        'SPEAKER': "\x21",
        'CLEAR/SET MEMORY': "\x24",
        'SET DAY OF WEEK': "\x26",
        'SET TIME FORMAT': "\x27",
        'SPEAKER TONE': "\x28",
        'RUN TIME TABLE': "\x29",
        'RESET': "\x2C",
        'RUN SEQUENCE': "\x2E",
        'DIMMING': "\x2F",
        'RUN DAY TABLE': "\x32",
        'CLEAR SERIAL ERROR REGISTER': "\x34",
        'SET COUNTER': "\x35",
        'SET ADDRESS': "\x37",
        'SET LARGE DOTS MEMORY CONFIG': "\x38",
        'APPEND TO LARGE DOTS MEMORY CONFIG': "\x39",
        'SET RUN FILE TIMES': "\x3A",
        'SET DATE': "\x3B",
        'CUSTOM CHARSET': "\x3C",
        'SET AUTOMODE TABLE': "\x3E",
        'SET DIMMING CONTROL REGISTER': "\x40",
        'SET COLOR CORRECTION': "\x43\x33",
        'SET CUSTOM COLOR CORRECTION': "\x43\x58",
        'SET TEMPERATURE OFFSET': "\x54",
        'SET UNIT COLUMNS AND ROWS': "\x55\x31",
        'SET UNIT RUN MODE': "\x55\x32",
        'SET UNIT SERIAL ADDRESS': "\x55\x33",
        'SET SERIAL DATA': "\x55\x34",
        'SET UNIT CONFIGURATION': "\x55\x35",
        'WRITE UNIT REGISTER': "\x55\x4E",
        'TOGGLE ACK/NAK RESPONSE': "\x73" }

    #Apperently you can configure when texts display
    START_STOP_TIMES = { 'ALL DAY': "FD",
        'NO TIMES': "FE",
        'ALL TIMES': "FF",
        'DAILY': "\x30",
        'SUNDAY': "\x31",
        'MONDAY': "\x32",
        'TUESDAY': "\x33",
        'WEDNESDAY': "\x34",
        'THURSDAY': "\x35",
        'FRIDAY': "\x36",
        'SATURDAY': "\x37",
        'MONDAY-FRIDAY': "\x38",
        'WEEKENDS': "\x39",
        'ALL DAYS': "\x41",
        'NO DAYS': "\x42" }

    # File label PRIORITY and 31 cannot be used as STRING labels
    # If the counter feature is used, the file labels 17 through 21 are reserved for target files
    FILE_LABELS = { 'PRIORITY': "\x30",
        '0': "\x30",
        '1': "\x20",
        '2': "\x21",
        '3': "\x22",
        '4': "\x23",
        '5': "\x24",
        '6': "\x25",
        '7': "\x26",
        '8': "\x27",
        '9': "\x28",
        '10': "\x29",
        '11': "\x2A",
        '12': "\x2B",
        '13': "\x2C",
        '14': "\x2D",
        '15': "\x2E",
        '16': "\x2F",
        '17': "\x31",
        '18': "\x32",
        '19': "\x33",
        '20': "\x34",
        '21': "\x35",
        '22': "\x36",
        '23': "\x37",
        '24': "\x38",
        '25': "\x39",
        '26': "\x3A",
        '27': "\x3B",
        '28': "\x3C",
        '29': "\x3D",
        '30': "\x3E",
        '31': "\x3F",
        '32': "\x40",
        '33': "\x41",
        '34': "\x42",
        '35': "\x43",
        '36': "\x44",
        '37': "\x45",
        '38': "\x46",
        '39': "\x47",
        '40': "\x48",
        '41': "\x49",
        '42': "\x4A",
        '43': "\x4B",
        '44': "\x4C",
        '45': "\x4D",
        '46': "\x4E",
        '47': "\x4F",
        '48': "\x50",
        '49': "\x51",
        '50': "\x52",
        '51': "\x53",
        '52': "\x54",
        '53': "\x55",
        '54': "\x56",
        '55': "\x57",
        '56': "\x58",
        '57': "\x59",
        '58': "\x5A",
        '59': "\x5B",
        '60': "\x5C",
        '61': "\x5D",
        '62': "\x5E",
        '63': "\x5F",
        '64': "\x60",
        '65': "\x61",
        '66': "\x62",
        '67': "\x63",
        '68': "\x64",
        '69': "\x65",
        '70': "\x66",
        '71': "\x67",
        '72': "\x68",
        '73': "\x69",
        '74': "\x6A",
        '75': "\x6B",
        '76': "\x6C",
        '77': "\x6D",
        '78': "\x6E",
        '79': "\x6F",
        '80': "\x70",
        '81': "\x71",
        '82': "\x72",
        '83': "\x73",
        '84': "\x74",
        '85': "\x75",
        '86': "\x76",
        '87': "\x77",
        '88': "\x78",
        '89': "\x79",
        '90': "\x7A",
        '91': "\x7B",
        '92': "\x7C",
        '93': "\x7D",
        '94': "\x7E"}

    # Meh... <italian_accent> maybe we need other modes later </italian_accent>
    WRITE_MODES = { 'ROTATE': "\x61",#Default
        'HOLD': "\x62",
        'FLASH': "\x63",
        'ROLL UP': "\x65",
        'ROLL DOWN': "\x66",
        'ROLL LEFT': "\x67",
        'ROLL RIGHT': "\x68",
        'WIPE UP': "\x69",
        'WIPE DOWN': "\x6A",
        'WIPE LEFT': "\x6B",
        'WIPE RIGHT': "\x6C",
        'SCROLL': "\x6D",
        'AUTOMODE': "\x6F",
        'ROLL IN': "\x70",
        'ROLL OUT': "\x71",
        'WIPE IN': "\x72",
        'WIPE OUT': "\x73",
        'COMPRESSED ROTATE': "\x74",
        'EXPLODE': "\x75",
        'CLOCK': "\x76",
        'TWINKLE': "\x6E\x30",
        'SPARKLE': "\x6E\x31",
        'SNOW': "\x6E\x32",
        'INTERLOCK': "\x6E\x33",
        'SWITCH': "\x6E\x34",
        'SLIDE': "\x6E\x35",
        'SPRAY': "\x6E\x36",
        'STARBURST': "\x6E\x37",
        'WELCOME': "\x6E\x38",
        'SLOT MACHINE': "\x6E\x39",
        'NEWS FLASH': "\x6E\x3A",
        'TRUMPET': "\x6E\x3B",
        'CYCLE COLORS': "\x6E\x43",
        'THANK YOU': "\x6E\x53",
        'NO SMOKING': "\x6E\x55",
        'DONT DRINK AND DRIVE': "\x6E\x56",
        'RUNNING ANIMALS OR FISH': "\x6E\x57",
        'FIREWORKS': "\x6E\x58",
        'BALLOON': "\x6E\x59",
        'CHERRY BOMB': "\x6E\x5A" }

    KEYBOARD_PROTECT = { 'UNLOCKED': "\x55", 'LOCKED': "\x4C" }#This is requierd for something.. I thnk there is some way to connect a keyboard to the sign
    FILE_TYPES = { 'TEXT': "\x41", 'STRING': "\x42", 'DOTS PICTURE': "\x44" }#Define a file as a TEXT, STRING, or picture
    TIME_FORMATS = { '12h': "\x53", '24h': "\x4D" }#Time formats
    COLOR_STATUS = { 'Monochrome': "1000", '3-color': "2000", '8-color': "4000" }#Color configure for dots pictures

    TEXT_MODE_START = '\x1B'#This is used for adding texts. This is put in front of the mode code to start the mode
    DISPLAY_POSITION = '0'

    TIME_DELAY = '<TIME_DELAY>'

    #Writing Text requires 3(4?) params: file, (display), mode, text
    #Writing String requires 2 params: file, string
    #Writing Dots picture requires 4 params: file, height, width, dots
    #Read Text 1 param: file
    #Read String 1 param: file
    #Read Dot 1 param: file
    #Write Special 2 params: function, var... params
        #Time uses 4 digits, 24 hour time as like 0001 or 1457
        #Clear/Set memory 5(can repeat): file, type, IRKeyboard, size, QQ
        #Set Day of week 1 param: day
        #Set Date 1 param: mmddyy
    #Read Special 1 param: which special function

    ''' END CONSTANTS '''

    def __init__(self, commandName, commandParams):
        self.commandName = commandName
        self.commandParams = commandParams
        self.value = None

    def construct(self):
        if self.commandName == 'WRITE TEXT':
            #Construct this command as writeText, in file, with display, display mode, and text
            self.value = (self.COMMAND_CODES['WRITE TEXT'] + self.FILE_LABELS[self.commandParams['fileLabel']] + TEXT_MODE_START + 
                self.commandParams['displayPosition'] + WRITE_MODES[self.commandParams['mode']] + self.commandParams['text'])
        elif self.commandName == 'WRITE STRING':
            self.value = self.COMMAND_CODES['WRITE STRING'] + self.FILE_LABELS[self.commandParams['fileLabel']] + self.commandParams['string']
        elif self.commandName == 'WRITE SMALL DOTS':
            self.value = (self.COMMAND_CODES['WRITE SMALL DOTS'] + self.FILE_LABELS[self.commandParams['fileLabel']] + 
                self.commandParams['height'] + self.commandParams['width'] + self.TIME_DELAY + self.commandParams['dots'])
    

    def getRawCommand(self):
        '''Returns the raw apcket with timeStops stripped out'''
        if self.value != None:
            return self.value.replace(self.TIME_DELAY, '')
        return None

    def getCommandParts(self):
        return (self.commandName, self.commandParams)

    def getCommand(self):
        return self.value
    
    @staticmethod
    def writeText(fileLabel, text, mode='HOLD', display=DISPLAY_POSITION):
        return command('WRITE TEXT', {'fileLabel' : fileLabel, 'text' : text, 'mode' : mode, 'displayPosition' : display})

    @staticmethod
    def writeString(fileLabel, string):
        return command('WRITE STRING', {'fileLabel' : fileLabel, 'string' : string})

    @staticmethod
    def writePicture(fileLabel, height, width, dots):
        return command('WRITE SMALL DOTS', {'fileLabel' : fileLabel, 'height' : height, 'width' : width, 'dots' : dots})
