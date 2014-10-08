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

@app.route('/spaces', methods=['POST'])
def requestFiles():
    global sqlite
    params = parseParams(request.stream.read())
    if params == False or not params['count']:
        return jsonify(result='failure', reason="missing count"), 412

    try:
        count = int(params['count'])
    except ValueError:
        return jsonify(result='failure', reason='count needs to be an int'), 412
    
    registration = sqlite.registerSpaces(count)

    if registration == False:
        return jsonify(results='failure', reason='Count is either too large or there is no space. Talk to an admin'), 412
   
    return jsonify(results='success', userKey=registration), 200
     

@app.route('/spaces', methods=['DELETE'])
def deleteFiles():
    global sqlite
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey()
    deleted = sqlite.deleteSpaces(key)
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/string', methods=['POST'])
def addStringToServer(fileLabel):
    global sqlite
    clear()
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey()

    files = sqlite.getFileLabels(key)

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412

    params = parseParams(request.stream.read())

    if params == False or not 'string' in params:
        return jsonify(result='failure', reason='No string given for string function'), 412

    string = re.sub(r'[^\x00-\x7F]+','', params['string']) 

    added = sqlite.registerSpaceAsString(files[fileLabel], string)

    #Start BetaBrite
    defineMemory()
    addStringToSign(files[fileLabel], string) 
    #End BetaBrite
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/text', methods=['POST'])
def addTextToServer(fileLabel):
    global sqlite
    clear()
    stringRegex = '<STRINGFILE:(\d+)>' 
    pictureRegex = '<PICTUREFILE:(\d+)>'
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
 
    for z in range(len(texts)):
        match = re.search(stringRegex, texts[z])
        if match:
            fileNum = int(match.group(1))
            if fileNum >= 0 and fileNum < len(files):
                texts[z] = re.sub(stringRegex, '\x10' + FILE_LABELS[files[fileNum]], texts[z])
        match = re.search(pictureRegex, texts[z])
        if match:
            fileNum = int(match.group(1))
            if fileNum >=0 and fileNum < len(files):
                texts[z] = re.sub(pictureRegex, '\x14' + FILE_LABELS[files[fileNum]], texts[z])

    sqlite.registerSpaceAsText(files[fileLabel], json.dumps({'texts':texts, 'modes':modes}))
    #Start BetaBrite
    defineMemory()
    addTextToSign(files[fileLabel], texts, modes) 
    #End BetaBrite
    return jsonify(results='success'), 204

@app.route('/spaces/<int:fileLabel>/picture', methods=['POST'])
def addDotPicture(fileLabel):
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
    width = params['width']
    height = params['height']
    if width <=0 or width > 255:
        return jsonify(result='failure', reason='Width must between 1 and 255 inclusive'), 412
    if height <=0 or height > 31:
        return jsonify(result='failure', reason='height must between 1 and 31 inclusive'), 412

    if not 'dots' in params or not isinstance(params['dots'], list):
        return jsonify(result='failure', reason='Need an array of dots to draw the picture'), 412

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

    sqlite.registerSpaceAsPicture(files[fileLabel], json.dumps({'height':height, 'width':width, 'dots':dots}))
    #Start BetaBrite
    defineMemory() 
    addPictureToSign(files['fileLabel'], height, width, dots) 
    #End BetaBrite
    return jsonify(result='success'),204

@app.route('/spaces/<int:fileLabel>', methods=['GET'])
def getSpace(fileLabel):
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
    
    return jsonify(result='success', type=space.type, value=space.value)

def addTextToSign(fileLabel, texts, modes):
    startPacket()
    startFile(fileLabel)
    for z in range(len(texts)):
        addText(texts[z], modes[z])
    
    endFile()
    endPacket()

def addStringToSign(fileLabel, string):
    startPacket()
    startFile(fileLabel, 'WRITE STRING')
    addString(string)
    endFile()
    endPacket()

def addPictureToSign(fileLabel, height, width,dots):
    startPacket()
    startFile(files['fileLabel'], 'WRITE SMALL DOT')
    addDotsPicture(files['fileLabel'], toHex(height), toHex(width), parseDots(dots))
    endFile()
    end()

def parseDots(dots):
    dot = ''
    delim = '\x0D'
    for dotRow in dots:
        dot += dotRow + delim
    return dot 

def defineMemory():
    global sqlite
    spaces =  sqlite.getRegisteredSpaces()
    startPacket()
    startSpecialFunction()
    startMemoryConfig()
    for space in spaces:
        if space.type == 'TEXT':
            text = json.loads(space.value)
            defineTextMemory(space.fileName, text['modes'], text['texts'])
        elif space.type == 'STRING':
            defineStringMemory(space.fileName, space.value)
        elif space.type == 'PICTURE':
            definePictureMemory(space.fileName, json.loads(space.value))
    end()
    time.sleep(.1)

def defineTextMemory(label, mode, text):
    size = 1 + sum(len(value) for value in text)
    size += sum(len(value) for value in mode) * 2 
    addTextConfig(label, size, 'ALL TIMES', 'NO TIMES')

def defineStringMemory(label, string):
    addStringConfig(label, len(string))

def definePictureMemory(label, value):
    addDotsPictureConfig(label, toHex(value['height']), toHex(value['width']))

def parseParams(rawBody):
    try:
        return json.loads(rawBody)
    except ValueError:
        return False

def toHex(num):
    return ("%x" % num).zfill(2)

def validKey(key):
    global sqlite
    return key and sqlite.validUser(key)  

def noKey():
    return jsonify(result='failure', reason='Invalid INFOSYS-KEY supplied'), 401

def updateSign():
    global sqlite
    texts, others =  sqlite.getRegisteredSpaces()
    for text in texts:
        pass

def startUp(test):
    global sqlite
    sqlite = sqlite()
    sqlite.setup()
    clearMemoryConfig()
    time.sleep(.1)
    defineMemory()
    updateSign()
    if test:
        app.debug = True
        app.run()
    else:
        app.debug = True
        app.run(host='0.0.0.0')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='InfoSys server config')
    parser.add_argument('-t', '--test', help = 'Run in test mode', action='store_true')
    args = parser.parse_args()
    startUp(args.test)
