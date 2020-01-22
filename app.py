import helper
from flask import Flask, jsonify, request, Response
import json
from flask import abort
import sqlite3
app = Flask(__name__)

tasks = [
            {
                'id' : 1,
                'title': u'Hello World'
            },
            {
                'id' : 2,
                'title': u'Bye World'
            }
        ]



@app.route('/', methods=['GET'])
def get_tasks():
    return "Welcome to Notes !"

@app.route('/todo_notes/get', methods=['GET'])
def get_all_items():
    res_data = helper.displayRows()
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response
   
@app.route('/todo_notes/get/<int:task_id>',methods=['GET'])
def get_task(task_id):
    res_data = helper.displayRowBasedOnId(task_id)
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/todo_notes/add', methods=['POST'])
def put_task():
    req_data = request.get_json()
    res_data = helper.addNotes(req_data)
    if res_data is None:
        response = Response("{'error': 'Item not added - '}"  + req_data, status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/todo_notes/update', methods=['PUT'])
def update_task():
    option = request.args.get('option', type = str)
    Id = request.args.get('id', type = int)
    value = request.args.get('value', type = str)
    res_data = helper.updateNotes(option, (value,Id))
    if res_data is None:
        response = Response("{'error': 'Item not added - '}"  + req_data, status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/todo_notes/delete', methods=['DELETE'])
def delete_task():
    Id = request.args.get('id',type = int )
    res_data = helper.deleteNotes(Id)
    if res_data is None:
        response = Response("{'error': 'Item not added - '}"  + req_data, status=400 , mimetype='application/json')
        return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=True)

