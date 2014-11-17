

class packet():

    '''Define constants'''
    NULL = '\0'#The packet start. Need at least five to get the signs attention and set the baud rate
    START_OF_HEADER = '\x01'#The start of header follows the nulls, used to signal the start of data
    START_OF_TEXT = '\x02'#The start of text, this is used to signify commands + data
    SIGN_ADDRESS = '00'#The address. 00 is used as the broadcast, or to all signs.
    END_OF_TRANSMISSION = '\x04'#This is the end of the packet.
    END_OF_TEXT = '\x03'#This is the end of a text. Used for sending nested packets

        #What sign type to send the packet to
    TYPE_CODES = {  'VISUAL VERIFICATION': "\x21",
        'SERIAL CLOCK': "\x22",
        'ALPHAVISION': "\x23",
        'FULL MATRIX ALPHAVISION': "\x24",
        'CHARACTER MATRIX ALPHAVISION': "\x25",
        'LINE MATRIX ALPHAVISION': "\x26",
        'RESPONDER': "\x30",
        'ONE-LINE SIGNS': "\x31",
        'TWO-LINE SIGNS': "\x32",
        '430i SIGN': "\x43",
        '440i SIGN': "\x44",
        '460i SIGN': "\x45",
        'ALPHAECLIPSE 3600 DISPLAY DRIVER': "\x46",
        'ALPHAECLIPSE 3600 TURBO ADAPTER': "\x47",
        'LIGHT SENSOR': "\x4C",
        '790i SIGN': "\x55",
        'ALPHAECLIPSE 3600': "\x56",
        'ALPHAECLIPSE TIME/TEMP': "\x57",
        'ALPHAPREMIERE 4000/9000': "\x58",
        'ALL SIGNS': "\x5A",#Default
        'BETABRITE SIGN': "\x5E",
        '4120C SIGN': "\x61",
        '4160C SIGN': "\x62",
        '4200C SIGN': "\x63",
        '4240C SIGN': "\x64",
        '215R SIGN': "\x65",
        '215C SIGN': "\x66",
        '4120R SIGN': "\x67",
        '4160R SIGN': "\x68",
        '4200R SIGN': "\x69",
        '4240R SIGN': "\x6A",
        '300 SERIES SIGN': "\x6B",
        '7000 SERIES SIGN': "\x6C",
        '96x16 MATRIX SOLAR SIGN': "\x6D",
        '128x16 MATRIX SOLAR SIGN': "\x6E",
        '160x16 MATRIX SOLAR SIGN': "\x6F",
        '192x16 MATRIX SOLAR SIGN': "\x70",
        'PPD SIGN': "\x71",
        'DIRECTOR SIGN': "\x72",
        '1006 DIGIT CONTROLLER': "\x73",
        '4080C SIGN': "\x74",
        '210C/220C SIGNS': "\x75",
        'ALPHAECLIPSE 3500 SIGNS': "\x76",
        'ALPHAECLIPSE 1500 TIME & TEMP SIGN': "\x77",
        'ALPHAPREMIERE 9000 SIGN': "\x78",
        'TEMPERATURE PROBE': "\x79",
        'ALL SIGNS WITH MEMORY CONFIGURED FOR 26 FILES': "\x7A" }
       
    '''End constants'''

    def __init__(self):
        self.signType = 'ALL SIGNS'
        self.port = '/dev/ttyUSB0'
        self.commands = []

    def setPort(self, port):
        self.port = port

    def setSignType(self, signType):
        if signType in self.TYPE_CODES:
            self.signType = signType

    def addCommand(self, command):
        pass

    def construct(self):
        pass

    def send(self):
        pass 
