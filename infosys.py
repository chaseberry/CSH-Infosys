import requests
import sys
import argparse
import json
class infosys():

    def __init__(self, key=None):
        self.key = key
        self.url = 'http://infosys.csh.rit.edu:5000/'

    def hasInfosysKey(func):
        def func_wrapper(self, *args):
            if not self.hasKey():
                raise Exception('No infosys key for this session')
            return func(self, *args)
        return func_wrapper

    def registerSpaces(self, count):
        if self.hasKey():
            return (False, 'There is already a key for this session')
        response = requests.post(self.url + 'spaces', data=json.dumps({'count':count}))
        jsonResponse = response.json()
        if response.status_code == 200:
            self.key=jsonResponse['userKey']
            return (True, jsonResponse['userKey'])
        return (False, jsonResponse['reason'])

    @hasInfosysKey
    def addText(self, space, text, mode='HOLD'):
        response = requests.post(self.url + 'spaces/' + space + '/text', data=json.dumps({'text':text, 'mode':mode}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Text added')
        jsonResponse = response.json()
        return (False, jsonResponse['reason'])
   
    @hasInfosysKey 
    def addString(self, space, string):
        response = requests.post(self.url + 'spaces/' + space + '/string', data=json.dumps({'string' : string}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'String added')
        jsonResponse = response.json()
        return (False, jsonResponse['reason'])

    @hasInfosysKey
    def addPicture(self, space, dots):
        try:
            width = len(dots[0])
            height = len(dots)
        except Exception:
            return (False, 'Dots is not a list of strings')

        response = requests.post(self.url + 'spaces/' + space + '/picture', data=json.dumps({'height' : height, 'width' : width, 'dots' : dots}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Picture added')

        jsonResponse = response.json()
        return (False, jsonResponse['reason'])

    @hasInfosysKey
    def addMultiText(self, space, textArray, modeArray):
        texts = []
        for z in range(len(textArray)):
            mode = 'HOLD'
            if modeArray[z]:
                mode = modeArray[z]
            texts.append({'text' : textArray[z], 'mode' : mode})

        response = requests.post(self.url + 'spaces/' + space + '/text', data=json.dumps({'multiText' : texts}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Texts added')

        jsonResponse = response.json()
        return (False, jsonResponse)

    @hasInfosysKey
    def getData(self, space):
        response = requests.get(self.url + 'spaces/' + space, headers={'X-INFOSYS-KEY' : self.key})
        jsonResponse = response.json()
        if response.status_code >= 200 and response.status_code <=299:
            return(True, jsonResponse)
        return(False, jsonResponse)

    @hasInfosysKey
    def deleteKey(self):
        response = requests.delete(self.url + 'spaces', headers={'X-INFOSYS-KEY' : self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            self.key = None
            return (True, {u'result' : u'success'})
        return (False, {u'result' : u'failure'})

    def hasKey(self):
        return not self.key == None

def printMenu():
    print('=============================') 
    print('|| r - register spaces     ||')
    print('|| t - post a text message ||')
    print('|| s - add a string file   ||')
    print('|| p - add a picture file  ||')
    print('|| m - post multi texts    ||')
    print('|| g - get saved data      ||')
    print('|| d - delete your key     ||')
    print('|| h - show this menu      ||')
    print('|| q - quit                ||')
    print('=============================')

#methods for dict

def getData():
    space = raw_input('Get data from what space? ')
    response = infosys.getData(space)
    print(response)

def registerSpaces():
    count = raw_input('How many slots do you wants? ')
    response = infosys.registerSpaces(count)
    print(response)

def addText():
    space = raw_input('Add a TEXT to what space? ')
    text = raw_input('The TEXT: ')
    if raw_input('Add a display mode? (y/n)') == 'y':
        mode = raw_input('MODE? ')
        response = infosys.addText(space, text, mode)
    else:
        response = infosys.addText(space, text)

    print(response)

def addString():
    space = raw_input('Add a STRING to what space? ')
    string = raw_input('The STRING: ')
    response = infosys.addString(space, string)
    print(response)

def addPicture():
    space = raw_input('Add a picture to what space? ')
    print('Please make your picture have a consistant height and width')
    print('Valid colors are 1-8, 0 is off, -1 is quit')
    rowCount = 1
    dots = []
    while True:
        row = raw_input('Dots for row ' + str(rowCount) + ': ')
        if row == '-1':
            break
        dots.append(row)
        rowCount += 1

    response = infosys.addPicture(space, dots)
    print(response)

def addMultiText():
    space = raw_input('Add texts to what spaces? ')
    texts = []
    modes = []
    while True:
        text = raw_input('The TEXT (-1 to quite): ')
        if text == '-1':
            break;
        if raw_input('Add a display MODE? (y/n) ') == 'y':
            mode = raw_input('The display MODE: ')
            modes.append(mode)
        else:
            modes.append('HOLD')
        texts.append(text)
   
    response = infosys.addMultiText(space, texts, modes)
    print(response) 

def deleteKey():
    response = infosys.deleteKey()
    print(response)

#end dict methods

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='InfoSys client config')
    parser.add_argument('-k', '--key', help = 'An infosys key')
    args = parser.parse_args()
    infosys = infosys(args.key)
    
    commands = {
        'h' : printMenu,
        'r' : registerSpaces,
        'g' : getData,
        't' : addText,
        's' : addString,
        'p' : addPicture,
        'd' : deleteKey,
        'm' : addMultiText
        }
    
    printMenu()
    while True:
        choice = raw_input('What do you want to do? ')
        
        if choice == 'q':
            sys.exit()
      
        if not choice in commands:
            print('\'' + choice + '\' is not a valid command. Type h to see more')
            continue

        try:
            commands[choice]()
        except Exception as e:
            print('Exception occured')
            print(e)
