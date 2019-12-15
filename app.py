from flask import Flask, request, render_template, redirect, url_for
from werkzeug.datastructures import ImmutableMultiDict

from database import Database
from jinja2 import Template

app = Flask(__name__)
db = Database('sqlite.db')

# Node types
PARAMETER = 'Parameter'
PLACE = 'Place'
SENSOR = 'Sensor'
VALUE = 'Value'

LABEL = ['sens', 'miasto', 'wartość', 'czas', 'parametr']

NEW_MEASURE = {}
DATA_TO_DELETE_FORM = []

##### GET


@app.route('/', methods=['GET'])
def redirect_index():
    return redirect(url_for('index'))


@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/measures/', methods=['GET'])
def get_measures():
    all_meas = db.get_all_measurements()
    print(all_meas)
    DATA_TO_DELETE_FORM.extend(all_meas)
    print(DATA_TO_DELETE_FORM)
    return render_template('measures.html',
                           label=LABEL,
                           data=all_meas)


@app.route('/get_measures_params/', methods=['GET'])
def get_measures_params():
    parameters = db.get_names_all_nodes_of_type(PARAMETER)
    places = db.get_names_all_nodes_of_type(PLACE)
    sensors = db.get_names_all_nodes_of_type(SENSOR)
    return render_template('get_measures_params.html',
                           parameters=parameters,
                           places=places,
                           sensors=sensors)


@app.route('/new_measure_choose_sensor/', methods=['GET'])
def new_measure_choose_sensor():
    sensors = db.get_names_all_nodes_of_type(SENSOR)
    return render_template('new_measure_choose_sensor.html', sensors=sensors)


##### POST


@app.route('/new_measure_choose_param/', methods=['POST'])
def new_measure_choose_param():
    sensor = request.form[SENSOR]
    NEW_MEASURE[SENSOR] = sensor
    params = db.get_sens_params(sensor)
    return render_template('new_measure_choose_param.html', parameters=params)


@app.route('/new_measure_value/', methods=['POST'])
def new_measure_value():
    param = request.form[PARAMETER]
    NEW_MEASURE[PARAMETER] = param
    return render_template('new_measure_value.html')


@app.route('/new_measure/', methods=['POST'])
def new_measure():
    value = request.form[VALUE]
    NEW_MEASURE[VALUE] = value

    db.insert(NEW_MEASURE)
    NEW_MEASURE.clear()

    return redirect(url_for('index'))


@app.route('/parametrized_measure/', methods=['POST'])
def parametrized_measure():
    parameter = request.form[PARAMETER]
    place = request.form[PLACE]
    sensor = request.form[SENSOR]
    out = db.get_measurements_for_selected_nodes(parameter, place, sensor)
    return render_template('measures_parametrized.html', label=LABEL, data=out)


@app.route('/delete/', methods=['POST'])
def delete():
    parameter = request.form
    for i in parameter.keys():
        elem_to_del_index = int(i)
    print(elem_to_del_index)
    if len(DATA_TO_DELETE_FORM) == 0:
        DATA_TO_DELETE_FORM.extend(db.get_all_measurements())
    print(DATA_TO_DELETE_FORM)
    print(DATA_TO_DELETE_FORM[elem_to_del_index])
    value = DATA_TO_DELETE_FORM[elem_to_del_index][2]
    time = DATA_TO_DELETE_FORM[elem_to_del_index][3]
    db.remove_measurement(value, time)
    DATA_TO_DELETE_FORM.clear()
    return redirect(url_for('index'))


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
