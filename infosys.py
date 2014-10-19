import requests

class infosys():

    self.url = 'https://infosys.csh.rit.edu:5000/'

    def registerSpaces(self, count):
        response = requests.post(self.url + 'spaces', json={'count':count})
        jsonResponse = response.json()
        if response.status_code == 200:
            return (True, jsonResponse['key'])
        return (False, jsonResponse['reason'])

    def addText(self, space, text, mode='HOLD'):
        response = requests.post(self.url + 'spaces/' + space + '/text', json={'text':text, 'mode':mode})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Text added')
        jsonResponse = response.json()
        return (False, jsonResponse['reason'])
    
    def addString(self, space, string):
        response = requests.post(self.url + 'spaces/' + space + '/string', json={'string' : string})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'String added')
        jsonResponse = response.json()
        return (False, jsonResponse['reason'])

    def addPicture(self, space, dots):
        try:
            width = len(dots[0])
            height = len(dots)
        except Exception:
            return (False, 'Dots is not in correct format')

        response = requests.post(self.url + 'spaces/' + space + '/picture', json={'height' : height, 'width' : width, 'dots' : dots})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Picture added')

        jsonResponse = response.json()
        return (False, jsonResponse['reason'])

    def addMultiText(self, space, textArray, modeArray):
        texts = []
        for z in range(len(textArray)):
            mode = 'HOLD'
            if modeArray[z]:
                mode = modeArray[z]
            texts.append({'text' : textArray[z], 'mode' : mode})

        response = requests.post(self.url + 'spaces/' + space + '/text', json={'multi' : texts})
        if response.status_code >= 200 and response.status_code <= 299:
            return (True, 'Picture added')

        jsonResponse = response.json()
        return (False, jsonResponse['reason'])
