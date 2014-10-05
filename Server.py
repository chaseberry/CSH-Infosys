from flask import Flask
from flask import jsonify 

app = flask(__name__)

@app.route('/spaces', methods=['POST'])
def requestFiles():
    if not request.form['count']:
        return jsonify(result='failure', reason="missing count"), 412
    
    try:
        count = int(request.form['count'])
    except ValueError:
        return jsonify(result='failure', reason='count needs to be an int'), 412
        
     

@app.route('/spaces', methods=['DELETE'])
def deleteFiles():
    return 'nope'

if __name__ == "__main__":
    app.run()
