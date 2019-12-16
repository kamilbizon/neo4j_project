from py2neo import Graph, Node, Relationship
from datetime import datetime

# Node types
PARAMETER = 'Parameter'
PLACE = 'Place'
SENSOR = 'Sensor'
VALUE = 'Value'


def _create_and_return_greeting(tx, message):
    result = tx.run("CREATE (a:Greeting) "
                    "SET a.message = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=message)
    return result.single()[0]


class Database:
    def __init__(self):
        self.gdb = Graph(auth=('neo4j', 'Passw0rd'))
        print(self.gdb)

    def get_names_all_nodes_of_type(self, node_type):
        nodes = self.gdb.nodes.match(node_type)
        nodes_names = [i["name"] for i in nodes]
        return nodes_names

    def get_node(self, node_type, name):
        node = self.gdb.nodes.match(node_type, name=name).first()
        return node

    def get_value(self, value, time):
        node = self.gdb.nodes.match(VALUE, value=value, time=time).first()
        return node

    def get_all_measurements(self):
        sensors = self.gdb.nodes.match("Sensor")
        table = []

        for sensor in sensors:
            sens_and_city = []
            all_rows = []

            #find where is placed
            sens_and_city.append(sensor['name'])
            sens_and_city_rel = self.gdb.match((sensor,), r_type='IS_PLACED_IN')
            for sens_city in sens_and_city_rel:
                sens_and_city.append(sens_city.end_node["name"])

            sens_and_meas_rel = self.gdb.match((None, sensor), r_type='WAS_MEASURED_BY')
            if len(sens_and_meas_rel) == 0:
                all_rows.append(sens_and_city)

            for measure_sens in sens_and_meas_rel:
                measure = measure_sens.nodes[0]

                whole_row = []
                whole_row.extend(sens_and_city)
                whole_row.append(measure["value"])
                whole_row.append(measure["time"])

                meas_parameter_rel = self.gdb.match((measure,), r_type='REPRESENTS')
                for param in meas_parameter_rel:
                    whole_row.append(param.end_node["name"])
                all_rows.append(whole_row)

            table.extend(all_rows)

        return table

    def get_sens_params(self, sensor):
        sensor = self.gdb.nodes.match("Sensor", name=sensor).first()
        relations = self.gdb.match((sensor,), r_type='MEASURES')
        
        result = []
        for rel in relations:
            result.append(rel.end_node["name"])

        return result

    def get_measurements_for_selected_nodes(self, parameter, place, sensor):
        sensors = self.gdb.nodes.match("Sensor", name=sensor)
        table = []

        for sensor in sensors:
            sens_and_city = []
            all_rows = []

            #find where is placed
            sens_and_city.append(sensor['name'])
            sens_and_city_rel = self.gdb.match((sensor,), r_type='IS_PLACED_IN')

            if len(sens_and_city_rel) == 0:
                return [[]]

            for sens_city in sens_and_city_rel:
                if sens_city.end_node["name"] != place:
                    return [[]]

                sens_and_city.append(sens_city.end_node["name"])

            sens_and_meas_rel = self.gdb.match((None, sensor), r_type='WAS_MEASURED_BY')
            if len(sens_and_meas_rel) == 0:
                all_rows.append(sens_and_city)

            for measure_sens in sens_and_meas_rel:
                measure = measure_sens.nodes[0]

                whole_row = []
                whole_row.extend(sens_and_city)
                whole_row.append(measure["value"])
                whole_row.append(measure["time"])

                meas_parameter_rel = self.gdb.match((measure,), r_type='REPRESENTS')
                should_add = False
                for param in meas_parameter_rel:
                    if param.end_node["name"] == parameter:
                        whole_row.append(param.end_node["name"])
                        should_add = True
                if should_add:
                    all_rows.append(whole_row)

            table.extend(all_rows)
        return table

    def insert(self, new_request):
        time = str(datetime.now().hour) + ':' + str(datetime.now().minute)
        node = Node(VALUE, value=new_request[VALUE], time=time)
        sensor = self.get_node(SENSOR, new_request[SENSOR])
        param = self.get_node(PARAMETER, new_request[PARAMETER])

        node_sensor = Relationship(node, "WAS_MEASURED_BY", sensor)
        node_param = Relationship(node, "REPRESENTS", param)
        self.gdb.create(node_sensor)
        self.gdb.create(node_param)

    def remove_measurement(self, value, time):
        node = self.get_value(value, time)
        print("DELETING:", node)
        self.gdb.delete(node)
