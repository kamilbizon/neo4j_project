from flask import Flask, request
from database import Database

app = Flask(__name__)
db = Database('sqlite.db')


##### GET


@app.route('/pomiar/', methods=['GET'])
def return_all_notes():
    return db.get_table("pomiar")


@app.route('/pomiar/<urzadzenie>/', methods=['GET'])
def return_notes_from_category(urzadzenie):
    where = "urzadzenie='" + urzadzenie + "'"
    return db.get_table("pomiar", where)


@app.route('/pomiar/<urzadzenie>/<data1>/<data2>/', methods=['GET'])
def return_notes_from_category_in_dates(urzadzenie, data1, data2):
    where = "urzadzenie='" + urzadzenie + "' "
    where += " AND "
    where += "data >= '" + data1 + "' "
    where += " AND "
    where += "data <= '" + data2 + "' "
    return db.get_table("pomiar", where)


##### POST


@app.route('/pomiar/<urzadzenie>/', methods=['POST'])
def save_note_to_category(urzadzenie):
    json = request.get_json()
    print(json)
    return db.insert_row("pomiar", json)


##### DELETE


@app.route('/pomiar/<urzadzenie>/<data1>/<data2>/', methods=['DELETE'])
def delete_note_form_category_with_id(urzadzenie, data1, data2):
    where = "urzadzenie = '" + urzadzenie + "' "
    where += " AND "
    where += "data>= '" + data1 + "' "
    where += " AND "
    where += "data<= '" + data2 + "' "
    return db.delete_row("pomiar", where)


##### PUT

@app.route('/pomiar/<urzadzenie>/<id>/', methods=['PUT'])
def change_note_from_category_with_id(urzadzenie, id):
    json = request.get_json()
    print(json)
    where = "id = " + id
    return db.update_row("pomiar", json, where)


##### CORS

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


#####


if __name__ == '__main__':
    # app.run(port=5579)
    pass
