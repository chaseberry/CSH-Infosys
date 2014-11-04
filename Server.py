from flask import Flask
from flask import jsonify 
from flask import request
from sqlite import sqlite
from BetaBrite import *
from BetaBriteSpace import BetaBriteSpace
import json
import argparse
import time
import re

app = Flask(__name__)
''' Start with sudo nohup python Server.py & '''

@app.errorhandler(404)
def url_not_found(e):
    return jsonify(result='failure', reason='URL not found. Please make sure your url is correct and your space is a number')

@app.route('/spaces', methods=['POST'])
def requestFiles():
    '''The url to request spaces. '''
    global sqlite
    params = parseParams(request.stream.read())#Param parsing from JSON in
    if params == False or not params['count']:
        return jsonify(result='failure', reason="missing count"), 412

    try:
        count = int(params['count'])
    except ValueError:
        return jsonify(result='failure', reason='count needs to be an int'), 412
    
    registration = sqlite.registerSpaces(count)#register count spaces to a specific key

    if registration == False:
        return jsonify(result='failure', reason='Count is either too large or there is no space. Talk to an admin'), 412
   
    return jsonify(result='success', userKey=registration), 200 #return the userKey + a 200
     

@app.route('/spaces', methods=['DELETE'])
def deleteFiles():
    '''Un-auth the specific key. This will clear, and free up the spaces to be used by someone else'''
    global sqlite
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey()
    deleted = sqlite.deleteSpaces(key)
    
    clearMemoryConfig()
    time.sleep(.1)
    updateSign()

    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/string', methods=['POST'])
def addStringToServer(fileLabel):
    '''Sets the specific file to a string'''
    global sqlite
    clear()#resets the BetaBritePacket in case something went wrong 
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey()

    files = sqlite.getFileLabels(key)#Get the list of files the user has access to

    if fileLabel < 0 or fileLabel >= len(files): #invalid file space check
        return jsonify(result='failure', reason='file label is out of bounds'), 412

    params = parseParams(request.stream.read())

    if params == False or not 'string' in params:
        return jsonify(result='failure', reason='No string given for string function'), 412

    string = re.sub(r'[^\x00-\x7F]+','', params['string'])#remove non-ASCII characters from the input string

    added = sqlite.registerSpaceAsString(files[fileLabel], string)#Register the given file to the sqlite DB

    #Start BetaBrite
    defineMemory()
    addStringToSign(files[fileLabel], string) 
    #End BetaBrite
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/text', methods=['POST'])
def addTextToServer(fileLabel):
    '''Sets the specific file to a text file'''
    global sqlite
    clear()
    stringRegex = '<STRINGFILE:(\d+)>'#A regex for the stringfile mod
    pictureRegex = '<PICTUREFILE:(\d+)>'#A regex for the picturefile mod
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey() 

    files = sqlite.getFileLabels(key)

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412 
   
    params = parseParams(request.stream.read())
    
    if params == False or (not 'text' in params and not 'multiText' in params):
        return jsonify(result='failure', reason='No \'text\' or \'multiText\' given for text function'), 412
    multi = False
    if 'multiText' in params:
        multi = True

    modes = []
    texts = []
    '''Parsing the given text/mod or multitext input'''
    if multi:
        for text in params['multiText']:
            if not 'text' in text:
                continue
            mode = 'HOLD'
            if 'mode' in text and text['mode'] in WRITE_MODES:
                mode = text['mode']
            modes.append(mode)

            texts.append(re.sub(r'[^\x00-\x7F]+','', text['text']))
    else:
        mode = 'HOLD'
        if 'mode' in params and params['mode'] in WRITE_MODES:
            mode = params['mode']
        modes.append(mode)
        texts.append(re.sub(r'[^\x00-\x7F]+','', params['text']))
 
    '''Regex matching for the specific files. Will replace the regexes and fileLabels with the correct transfercode and FILELABEL'''
    for z in range(len(texts)):
        match = re.search(stringRegex, texts[z])
        
        while match != None:
            fileNum = int(match.group(1))
            if fileNum >= 0 and fileNum < len(files):
                texts[z] = re.sub(stringRegex, '\x10' + FILE_LABELS[files[fileNum]], texts[z], 1)
            else:
                return jsonify(result='failure', reason='Invalid space given for <STRINGFILE:#>'), 409
            match = re.search(stringRegex, texts[z])

        match = re.search(pictureRegex, texts[z])
        while match:
            fileNum = int(match.group(1))
            if fileNum >=0 and fileNum < len(files):
                texts[z] = re.sub(pictureRegex, '\x14' + FILE_LABELS[files[fileNum]], texts[z], 1)
            else:
                return jsonify(result='failure', reason='Invalid space given for <STRINGFILE:#>'), 409
            match = re.search(pictureRegex, texts[z])

    sqlite.registerSpaceAsText(files[fileLabel], json.dumps({'texts':texts, 'modes':modes}))#Register the space as a Text start. Value is stored as json
    #Start BetaBrite
    defineMemory()
    addTextToSign(files[fileLabel], texts, modes) 
    #End BetaBrite
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/picture', methods=['POST'])
def addDotPicture(fileLabel):
    '''Add the specific space as a picture'''
    global sqlite
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey() 

    files = sqlite.getFileLabels(key)

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412 
   
    params = parseParams(request.stream.read())
    if params == False or not 'width' in params or not 'height' in params:
        return jsonify(result='failure', reason='Need to give a width and a height'), 412
    
    '''Parsing height and width and size checking'''
    width = params['width']
    height = params['height']
    if width <=0 or width > 255:
        return jsonify(result='failure', reason='Width must between 1 and 255 inclusive'), 412
    if height <=0 or height > 31:
        return jsonify(result='failure', reason='height must between 1 and 31 inclusive'), 412

    if not 'dots' in params or not isinstance(params['dots'], list):
        return jsonify(result='failure', reason='Need an array of dots to draw the picture'), 412

    '''Parsing of the given dots. This makes sure tehre are the proper number of rows and columns. Makes sure each \'dot\' is a number
        and that each input is a String'''
    dots = []
    numHeight = 0
    for dotRow in params['dots']:
        numHeight += 1
        numWidth = 0
        try:
            for dot in dotRow:
                numWidth += 1
                try:
                    if int(dot) < 0 or int(dot) > 8:
                        return jsonify(result='faulure', reason='each \'dot\' must be a number between 0 and 8 inclusive'), 412
                except Exception:
                    return jsonify(result='faulure', reason='each \'dot\' must be a number between 0 and 8 inclusive'), 412
                
        
        except Exception:
            return jsonify(result='failure', reason='Each row must be a string'), 412
      
        if numWidth != width:
            return jsonify(result='failure', reason='Each row must be ' + str(width) + ' long'), 412  
       
        dots.append(dotRow) 
       
    if len(dots) != height:
        return jsonify(result='failure', reason='You must have ' + str(height) + ' rows'), 412

    sqlite.registerSpaceAsPicture(files[fileLabel], json.dumps({'height':height, 'width':width, 'dots':dots}))#Saves the given space as a picture space
    #Start BetaBrite
    defineMemory() 
    addPictureToSign(files[fileLabel], height, width, dots) 
    #End BetaBrite
    return jsonify(result='success'),204

@app.route('/spaces/<int:fileLabel>', methods=['GET'])
def getSpace(fileLabel):
    '''Gets the data stored at the given fileLabel(space). NOTE: This only comes from the sqlite database. If something happens to the sign. eh?'''
    global sqlite
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey() 

    files = sqlite.getFileLabels(key)

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='Space label is out of bounds'), 412
  
    space = sqlite.getSpace(files[fileLabel])
    if space == None:
        return jsonify(result='failure', reason='Space does not exist'), 412
    
    return jsonify(result='success', type=space.type, value=space.value)#Note if the type is a TEXT or a PICTURE the data returned is JSON

def addTextToSign(fileLabel, texts, modes):
    '''Add an array of texts and modes to the sign'''
    clear()
    startPacket()#starts the packet
    startFile(fileLabel)#starts the file at the given file label
    for z in range(len(texts)):
        addText(texts[z], modes[z])#adds the given text/mode objects to the sign
    
    endFile()#ends file
    endPacket()#ends and sends file

def addStringToSign(fileLabel, string):
    '''Adds a string to a a stringfile'''
    clear()
    startPacket()
    startFile(fileLabel, 'WRITE STRING')#Starts the file as a STRING file
    addString(string)
    endFile()
    endPacket()

def addPictureToSign(fileLabel, height, width, dots):
    '''Adds a picture to a picture file'''
    clear()
    startPacket()
    startFile(fileLabel, 'WRITE SMALL DOTS')#Starts the file as a SMALL DOT file
    addDotsPicture(fileLabel, toHex(height), toHex(width), parseDots(dots))#Adds the height, width, and dots to the file
    endFile()
    end()

def parseDots(dots):
    '''Takes an array of dots(where each is a string) and builds the string with <CR>s to send to the sign'''
    dot = ''
    delim = '\x0D'
    for dotRow in dots:
        dot += dotRow + delim
    return dot 

def defineMemory():
    '''Sends all memory configs to the sign in one GIANT packet'''
    global sqlite
    spaces =  sqlite.getUsedSpaces()#Gets all spaces with users and TYPEs != None
    startPacket()
    startSpecialFunction()
    startMemoryConfig()
    for space in spaces:
        if space.type == 'TEXT':
            text = json.loads(space.value)#load the text value from the space as json
            defineTextMemory(space.fileName, text['modes'], text['texts'])#adds the textMemory to the packet
        elif space.type == 'STRING':
            defineStringMemory(space.fileName, space.value)#adds the stringMemory to the packet
        elif space.type == 'PICTURE':
            definePictureMemory(space.fileName, json.loads(space.value))#adds the pictureMemory to the packet
    end()
    time.sleep(.1)#You need a delay between packets to keep the sign from crashing

def defineTextMemory(label, mode, text):
    '''Creates the packet config for the textmemroy.'''
    size = 1 + sum(len(value) for value in text)
    size += sum(len(value) for value in mode) * 2 
    addTextConfig(label, size, 'ALL TIMES', 'NO TIMES')

def defineStringMemory(label, string):
    '''Creates the packet config for the stringmemory.'''
    addStringConfig(label, len(string))

def definePictureMemory(label, value):
    '''Creates the packet config for the picturememory'''
    addDotsPictureConfig(label, toHex(value['height']), toHex(value['width']))

def parseParams(rawBody):
    '''Return the json object loaded from the rawBody of the http request'''
    try:
        return json.loads(rawBody)
    except ValueError:
        return False

def toHex(num):
    '''Converts an base10 number to a hex value with two bytes, even if only 1 byte is not 0'''
    return ("%x" % num).zfill(2)

def validKey(key):
    '''Checks the validity of the key.'''
    global sqlite
    return key and sqlite.validUser(key)  

def noKey():
    '''Creates a flaskReturn object for an invalid infosys-key'''
    return jsonify(result='failure', reason='Invalid INFOSYS-KEY supplied'), 401

def updateSign():
    '''Does a complete refresh of the sign from the data stored in the sqlite db
        Finds all spaces with TEXT and loads them to the sigh. Then loads the String and Picture files to the sign'''
    global sqlite
    defineMemory()
    spaces =  sqlite.getTextandOtherSpaces()#gets the text and not-text spaces
    texts = spaces[0]
    others = spaces[1]
    for text in texts:
        textData = json.loads(text.value)
        addTextToSign(text.fileName, textData['texts'], textData['modes'])#add the text to the sign

    for other in others:
        if other.type == 'STRING':
            addStringToSign(other.fileName, other.value)#add the string to the sign
        elif other.type == 'PICTURE':
            pictureData = json.loads(other.value)
            addPictureToSign(other.fileName, pictureData['height'], pictureData['width'], pictureData['dots'])#add the picture to the sign 

def startUp(test):
    '''Startup function with a test flag
        This creates the sqlite connection as well as clearing the sign and re-creating it from what is in the sqlite db'''
    global sqlite
    sqlite = sqlite()
    sqlite.setup()
    clearMemoryConfig()
    time.sleep(.1)
    updateSign()
    if test:
        app.debug = True
        app.run()
    else:
        app.run(host='0.0.0.0')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='InfoSys server config')
    parser.add_argument('-t', '--test', help = 'Run in test mode', action='store_true')
    args = parser.parse_args()
    startUp(args.test)
