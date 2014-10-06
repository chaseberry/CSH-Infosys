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

@app.route('/spaces/<int:fileLabel>/strings', methods=['POST'])
def addStringToServer(fileLabel):
    global sqlite
    key = request.headers.get('X-INFOSYS-KEY')
    if not validKey(key):
        return noKey()

    files = sqlite.getFileLabels(key)

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412

    params = parseParams(request.stream.read())

    if params == False or not 'string' in params:
        return jsonify(result='failure', reason='No string given for string function'), 412

    added = sqlite.registerSpaceAsString(files[fileLabel], params['string'])

    #Start BetaBrite
    defineMemory()
    startPacket()
    startFile(files[fileLabel], 'WRITE STRING')
    addString(params['string'])
    endFile()
    endPacket()
    #End BetaBrite
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/texts', methods=['POST'])
def addTextToServer(fileLabel):
    global sqlite
    regex = '<STRINGFILE:(\d+)>' 
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
            if 'mode' in params and params['mode'] in WRITE_MODES:
                mode = params['mode']
            modes.append(mode)
            texts.append(text['text'])
    else:
        mode = 'HOLD'
        if 'mode' in params and params['mode'] in WRITE_MODES:
            mode = params['mode']
        modes.append(mode)
        texts.append(params['text'])
 
    for z in range(len(texts)):
        match = re.search(regex, texts[z])
        if match:
            fileNum = int(match.group(1))
            if fileNum >= 0 and fileNum < len(files):
                texts[z] = re.sub(regex, '\x10' + FILE_LABELS[files[fileNum]], texts[z])

    sqlite.registerSpaceAsText(files[fileLabel], json.dumps({'texts':texts, 'modes':modes}))
    #Start BetaBrite
    defineMemory()
    startPacket()
    startFile(files[fileLabel])
    for z in range(len(texts)):
        addText(texts[z], modes[z])
    
    endFile()
    endPacket()
    #End BetaBrite
    return jsonify(results='success'), 204

@app.route('/clear', methods=['POST'])
def clearSign():
    global sqlite

    key = request.headers.get('X-INFOSYS-KEY')
    #is key admin
    #return noKey()
    clearMemoryConfig()
    return jsonify(result='success'), 204 

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
    end()
    time.sleep(.1)

def defineTextMemory(label, mode, text):
    size = 1 + sum(len(value) for value in text)
    size += sum(len(value) for value in mode) * 2 
    addTextConfig(label, size, 'ALL TIMES', 'NO TIMES')

def defineStringMemory(label, string):
    addStringConfig(label, len(string))

def parseParams(rawBody):
    try:
        return json.loads(rawBody)
    except ValueError:
        return False

def validKey(key):
    global sqlite
    return key and sqlite.validUser(key)  

def noKey():
    return jsonify(result='failure', reason='Invalid INFOSYS-KEY supplied'), 401

if __name__ == "__main__":
    global sqlite
    sqlite = sqlite()
    sqlite.setup()
    parser = argparse.ArgumentParser(description='InfoSys server config')
    parser.add_argument('-t', '--test', help = 'Run in test mode', action='store_true')
    args = parser.parse_args()
    if args.test:
        app.debug = True
        app.run()
    else:
        app.debug = True
        app.run(host='0.0.0.0')
