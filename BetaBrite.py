#!/usr/bin/python2

#BetaBrite.py
#Original author: Russell Harmon ( russ@csh.rit.edu, http://rus.har.mn )
# Soooo... yea.... this is not documented (much)... the API docs however are available =)
#Current maintainer: Josh McSavaney ( mcsaucy@csh.rit.edu )

import datetime

# The \0 chars are merely to get the device's attention
NULL = "\0"
START_OF_HEADER = "\x01"
ADDRESS = "00" # Broadcast
START_OF_TEXT = "\x02"
packet = ""
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

# Meh... <italian_accent> maybe we need other modes later </italian_accent>
WRITE_MODES = { 'ROTATE': "\x61",
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

TYPE_CODES = {  'VISUAL VERIFICATION': "\x21",
        'SERIAL CLOCK': "\x22",
        'ALPHAVISION': "\x23",
        'FULL MATRIX ALPHAVISION': "\x24",
        'CHARACTER MATRIX ALPHAVISION': "\x25",
        'LINE MATRIX ALPHAVISION': "\x26",
        'RESPONDER': "\x30",
        'ONE-LINE SIGNS': "\x31",
        'TWO-LINE SIGNS': "\x32",
        # There is already an all signs entry
        #'ALL SIGNS': "\x3F",
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
        'ALL SIGNS': "\x5A",
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
        '94': "\x7E",
        '1337': "This is our world now... the world of the electron and the switch, the beauty of the baud.  We make use of a service already existing without paying for what could be dirt-cheap if it wasn't run by profiteering gluttons, and you call us criminals.  We explore... and you call us criminals.  We seek after knowledge... and you call us criminals.  We exist without skin color, without nationality, without religious bias... and you call us criminals. You build atomic bombs, you wage wars, you murder, cheat, and lie to us and try to make us believe it's for our own good, yet we're the criminals. Yes, I am a criminal.  My crime is that of curiosity.  My crime is that of judging people by what they say and think, not what they look like. My crime is that of outsmarting you, something that you will never forgive me for. I am a hacker, and this is my manifesto.  You may stop this individual, but you can't stop us all... after all, we're all alike." }

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

KEYBOARD_PROTECT = { 'UNLOCKED': "\x55", 'LOCKED': "\x4C" }
FILE_TYPES = { 'TEXT': "\x41", 'STRING': "\x42", 'DOTS PICTURE': "\x44" }
TIME_FORMATS = { '12h': "\x53", '24h': "\x4D" }
COLOR_STATUS = { 'Monochrome': "1000", '3-color': "2000", '8-color': "4000" }

BRANCHES = { 'Packet': 'endPacket',
         'File': 'endFile',
         'Special Function': 'endSpecialFunction',
         'Memory Config': 'endMemoryConfig' }

START_MODE = "\x1B"
DISPLAY_POSITION = "0"
END_OF_TRANSMISSION = "\x04"
END_OF_TEXT = "\x03"

# The branch prevents you from calling functions that are of an entirely different set
branch = []
# The lock prevents you from adding multiple things to a packet that cannot go together
lock = 0
device = ""

def startPacket( address = ADDRESS, type = 'ALL SIGNS', port = "/dev/ttyUSB0" ):
    global branch, packet, device, lock
    packet = ""
    device = port
    type = TYPE_CODES[type]
    lock = 0
    if len(branch) == 0:
        packet += START_OF_HEADER + type + address + START_OF_TEXT
        branch.append( "Packet" )
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def endPacket( ):
    global packet, branch, device

    if len(branch) == 1:
        #packet += END_OF_TEXT
        #checksum =
        packet += END_OF_TRANSMISSION
        packet = NULL * 8 + packet
        file = open( device, "wb" )
        log = open( "/var/log/betabrite.txt", "wb" )
        file.write( packet )
        log.write( packet )
        log.write( "\n" )
        log.close()

        branch.pop()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def startFile( label, option='WRITE TEXT' ):
    global packet, branch, lock
    #This function will default to writing text, but it can be used to write STRINGs,
    #for example, by calling startFile("1", "WRITE STRING")

    if not option in COMMAND_CODES:
        #not a valid command
        return

    if len(branch) == 1 and branch[ len(branch) - 1 ] == "Packet" and lock == 0:
        packet += COMMAND_CODES[ option ] + FILE_LABELS[label]
        branch.append( option )
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def endFile():
    global branch, COMMAND

    if len(branch) == 2 and branch[ len(branch) - 1 ] in COMMAND_CODES:
        branch.pop()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def addText( text = "", mode = 'HOLD' ):
    global packet, branch

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "WRITE TEXT":
        packet += START_MODE + DISPLAY_POSITION + WRITE_MODES[mode] + text
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def setPriority( text = "", mode = 'HOLD' ):
    startPacket()
    startFile("0")
    addText(text)
    endFile()
    endPacket()

def removePriority():
    startPacket()
    startFile("0")
    endFile()
    endPacket()

def addString( text = "" ):
    global packet, branch, lock

    if lock == 1 and len(branch) == 2 and branch[ len(branch) -1 ] == "WRITE STRING":
        if len(text) > 125:
            text = text[:125]
            print "** WARNING **: STRINGs may only be 125 bytes in size. Truncating."
        packet += text
        lock +=1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def addDotsPicture( label, height = "07", width = "50", dots = "" ):
    global packet, branch
    #remember that at least 100 ms must have passed between receiving the width and first row
    if len(branch) == 2 and branch[ len(branch) - 1 ] == "WRITE SMALL DOTS":
        packet += "I" + FILE_LABELS[label] + height + width + dots
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def startSpecialFunction():
    global packet, branch, lock

    if len(branch) == 1 and branch[ len(branch) - 1 ] == "Packet" and lock == 0:
        packet += COMMAND_CODES['WRITE SPECIAL']
        branch.append( "Special Function" )
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def endSpecialFunction():
    global branch

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function":
        branch.pop()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def setDateTime( dateTime ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['SET TIME'] + str(dateTime.hour) + str(dateTime.minute)
        packet += SPECIAL_FUNCTIONS['SET DAY OF WEEK'] + str(dateTime.isoweekday)
        packet += SPECIAL_FUNCTIONS['SET DATE'] + str(dateTime.month) + str(dateTime.day) + str( dateTime.year )[2:]
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def softReset():
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['RESET']
        lock += 1
    elif len(branch) == 1 and branch[ len(branch) - 1 ] == "Packet" and lock == 0:
        startSpecialFunction()
        softReset()
        endSpecialFunction()
    elif len(branch) == 0:
        startPacket()
        softReset()
        endPacket()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def toggleSpeaker( state = True ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['SPEAKER']
        lock += 1
        if state:
            packet += "00"
        else:
            packet += "FF"
    else:
        raise PacketLevelException('Method called outside of branch restriction.')


def startMemoryConfig():
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['CLEAR/SET MEMORY']
        branch.append( "Memory Config" )
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def endMemoryConfig():
    global branch

    if len(branch) == 3 and branch[ len(branch) - 1 ] == "Memory Config":
        branch.pop()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def clearMemoryConfig():
    global packet, branch, lock
    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        lock += 1
        packet += SPECIAL_FUNCTIONS['CLEAR/SET MEMORY']
    elif len(branch) == 1 and branch[ len(branch) - 1 ] == "Packet" and lock == 0:
        startSpecialFunction()
        clearMemoryConfig()
        endSpecialFunction()
    elif len(branch) == 0:
        startPacket()
        clearMemoryConfig()
        endPacket()
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def addTextConfig( label, maxSize, startTime, stopTime, kbdProtect = 'LOCKED' ):
    global packet, branch, lock

    if len(branch) == 3 and branch[ len(branch) - 1 ] == "Memory Config" and lock == 2:
        # Even I don't know what the hell this is doing
        # What the hell this is doing:  converting the size into hex, making it a string, and padding it properly <3 McSaucy
        memSize = hex(int(maxSize))[2:].upper()
        while len(memSize) < 4:
            memSize = "0" + memSize
        print "Text Memory Size = " + memSize
        packet += FILE_LABELS[label] + FILE_TYPES['TEXT'] + KEYBOARD_PROTECT[kbdProtect] + memSize + START_STOP_TIMES[startTime] + START_STOP_TIMES[stopTime]
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def addStringConfig( stringLabel, maxStringSize = 125 ):
    
    global packet, branch, lock

    if len(branch) == 3 and branch[ len(branch) - 1 ] == "Memory Config" and lock == 2:
        
        if maxStringSize > 125:
            print "** WARNING **: STRINGs may only be 125 bytes in size. Setting size to be 125."
            maxStringSIze = "125"
        
        memSize = hex(int(maxStringSize))[2:].upper()
        while len(memSize) < 4:
            memSize = "0" + memSize
        print "String Memory Size = " + memSize

        packet += FILE_LABELS[stringLabel] + FILE_TYPES['STRING'] + "L" + memSize + "0000"
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def addDotsPictureConfig( label, pixelRows, pixelCols, colorStatus = '8-color', kbdProtect = 'LOCKED' ):
    global packet, branch, lock

    if len(branch) == 3 and branch[ len(branch) - 1 ] == "Memory Config" and lock == 2:
        packet +=  FILE_TYPES['DOTS PICTURE'] + FILE_LABELS[label] + str(pixelRows) + str(pixelCols) + COLOR_STATUS[colorStatus]
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def setRunTime( label, startTime, stopTime ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['RUN TIME TABLE'] + FILE_LABELS[label] + START_STOP_TIMES[startTime] + START_STOP_TIMES[stopTime]
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def setSerialAddress( address ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['SET ADDRESS'] + address
        lock += 1
    else:
        raise PacketLevelException('Method called outside of branch restriction.')

def setRunDay( label, startDay, stopDay ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        lock += 1
        packet += SPECIAL_FUNCTIONS['RUN DAY TABLE'] + FILE_LABELS[label] + START_STOP_TIMES[startDay] + START_STOP_TIMES[stopDay]
    else:
        print lock
        print len(branch)
        print branch[ len(branch) - 1 ]
        raise PacketLevelException('Method called outside of branch restriction.')

def setTimeFormat( military = False ):
    global packet, branch, lock

    if len(branch) == 2 and branch[ len(branch) - 1 ] == "Special Function" and lock == 1:
        packet += SPECIAL_FUNCTIONS['SET TIME FORMAT']
        lock += 1
        if military:
            packet += "M"
        else:
            packet += "S"

def clear():
    global packet, branch, device

    branch = []
    lock = 0
    packet = ""
    device = ""

# This method does something very cool... try to figure out what it is...
def end():
    global branch

    if len(branch) != 0:
        eval(BRANCHES[branch[-1]])()
        end()

def getLevel():
    global branch

    return branch

def rawData( data ):
    global packet, branch

    print "Don't be a douchebag -- only use this for testing. This means you, Scott."
    #legacy output message telling orange to use the actual functionality
    if len(branch) == 0:
        startPacket()
        packet += data
        endPacket()
    else:
        packet += data


class BetaBriteException( Exception ):
    def __init__( self, value ):
        self.value = value

    def __str__( self ):
        return repr( self.value )

class PacketLevelException( BetaBriteException ):
    def __init__( self, value ):
        self.value = value

    def __str__( self ):
        return repr( self.value )
