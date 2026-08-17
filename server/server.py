from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory
from flask_session import Session
import numpy as np
from node import Area, Pillar, Node, BlockNode, PathMap
#jsonify turns something into jsong to return, redirect goes to a new url,
#url_for gets the url for a method
app = Flask(__name__)
app.secret_key = 'yo'
app.config['SESSION_TYPE'] = 'filesystem' #Stores session data in a filesystem, allowing for storage of larger structures
Session(app)

@app.route('/')
def frontEnd():
    if(not("area" in session)):
        session["area"] = Area(10)

    return send_from_directory('../display', 'page.html')

@app.route('/api/getPath', methods=['GET'])
def get_path():
    path = session["path"]
    return jsonify(path)

@app.route('/api/makePath', methods=['POST'])
def store_path():
    data = request.get_json(force=True)

    a = session["area"]

    if((not checkValidPos(a, int(data['xStart']), int(data['yStart']))) or (not checkValidPos(a, int(data['xEnd']), int(data['yEnd'])))):
        session["path"] = []
        session.modified = True
        return jsonify({'message': 'gotchu'})

    start = Node(int(data['xStart']), int(data['yStart']), None, 0, None)
    end = Node(int(data['xEnd']), int(data['yEnd']), None, 0, None)
    map = PathMap(a, start, end)
    map.startPath()
    path = map.returnPath()
    toStore = []

    for node in path:
        toStore.append([node.posX, node.posY])

    session["path"] = toStore
    session.modified = True
    return jsonify({'message': 'gotchu'})


@app.route('/api/instruct', methods=['GET'])
def get_instruction():
    a = session["area"]
    return jsonify(a.instructGen())

@app.route('/api/postPillar', methods=['POST'])
def store_area():
    data = request.get_json(force=True)
    pSize = int(data['length'])
    xPos = int(data['x'])
    yPos = int(data['y'])
    a = session["area"]

    p = Pillar(1, pSize, pSize)
    a.place(xPos, yPos, p)

    session["area"] = a
    session.modified = True #tells session it has been modified
    return jsonify({'message': 'gotchu'})

@app.route('/api/clear', methods=['POST'])
def clear():
    session["area"] = Area(10)
    session.modified = True
    return jsonify({'message': 'recieved'})

def checkValidPos(a, x, y):
    length = len(a.area)
    if(x >= length or x < 0):
        return False
    if(y >= length or y < 0):
        return False

    return True
    

#Unused routes:()
#@app.route('/api/toServer', methods=['POST'])
#def print_data():
    #data = request.get_json(force=True)
    #print(data['message'])#data is actually a dictionary, so you need to use brackets to access, or use a .get method for safe access
    #return redirect(url_for('get_data')) #make sure function name is in quotes

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     return jsonify({"message": "Hello from Python!"})

# @app.route('/api/map', methods=['GET'])
# def get_map():
#     a = Area(100)
#     map = a.serialize()
#     return jsonify(map)
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)


