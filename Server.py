from flask import Flask
from flask import jsonify 
from flask import request
from sqlite import sqlite

app = Flask(__name__)

@app.route('/spaces', methods=['POST'])
def requestFiles():
    global sqlite
    if not 'count' in request.form:
        return jsonify(result='failure', reason="missing count"), 412

    try:
        count = int(request.form['count'])
    except ValueError:
        return jsonify(result='failure', reason='count needs to be an int'), 412
    
    registration = sqlite.registerSpaces(count)

    if registration == False:
        return jsonify(results='failure', reason='Count is either too large or there is no space. Talk to an admin'), 412
   
    return jsonify(results='success', userKey=registration), 200
     

@app.route('/spaces', methods=['DELETE'])
def deleteFiles():
    return 'nope'

if __name__ == "__main__":
    global sqlite
    sqlite = sqlite()
    sqlite.setup()
    app.debug = True
    app.run()

