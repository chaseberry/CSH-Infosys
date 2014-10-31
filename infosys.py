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
        print(jsonResponse)
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
        if self.key == None:
            return(False, 'There is no infosys key for this session')
        try:
            width = len(dots[0])
            height = len(dots)
        except Exception:
            return (False, 'Dots is not a list of lists')

        response = requests.post(self.url + 'spaces/' + space + '/picture', data=json.dumps({'height' : height, 'width' : width, 'dots' : dots}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Picture added')

        jsonResponse = response.json()
        return (False, jsonResponse['reason'])

    @hasInfosysKey
    def addMultiText(self, space, textArray, modeArray):
        if self.key == None:
            return(False, 'There is no infosys key for this session')
        texts = []
        for z in range(len(textArray)):
            mode = 'HOLD'
            if modeArray[z]:
                mode = modeArray[z]
            texts.append({'text' : textArray[z], 'mode' : mode})

        response = requests.post(self.url + 'spaces/' + space + '/text', data=json.dumps({'multi' : texts}), headers={'X-INFOSYS-KEY':self.key})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Picture added')

        jsonResponse = response.json()
        return (False, jsonResponse)

    @hasInfosysKey
    def getData(self, space):
        response = requests.get(self.url + 'spaces/' + space, headers={'X-INFOSYS-KEY' : self.key})
        jsonResponse = response.json()
        if response.status_code >= 200 and response.status_code <=299:
            return(True, jsonResponse)
        return(False, jsonResponse)

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
#end dict methods

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='InfoSys client config')
    parser.add_argument('-k', '--key', help = 'An infosys key')
    args = parser.parse_args()
    infosys = infosys(args.key)
    printMenu()
    while True:
        choice = raw_input('What do you want to do? ')
        
        if choice == 'q':
            sys.exit()

        elif choice == 'r' and infosys.hasKey():
            print('You already have a key in this session!')
       
        elif choice == 'g':
            getData()  
            
        elif choice == 'r':
            registerSpaces() 
        
