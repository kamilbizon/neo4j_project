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
    def __init__(self, connect):
        self.gdb = Graph(auth=('neo4j', 'Passw0rd'))
        print(self.gdb)

    def get_names_all_nodes_of_type(self, node_type):
        nodes = self.gdb.nodes.match(node_type)
        nodes_names = [i["name"] for i in nodes]
        return nodes_names

    def get_node(self, node_type, name):
        node = self.gdb.nodes.match(node_type, name=name).first()
        return node

    def get_all_measurements(self):
        sensors = self.gdb.nodes.match("Sensor")
        table = []

        for sensor in sensors:
            sens_and_city = []
            all_rows = []
            print(sensor)

            #find where is placed
            sens_and_city.append(sensor['name'])
            sens_and_city_rel = self.gdb.match((sensor,), r_type='IS_PLACED_IN')
            for sens_city in sens_and_city_rel:
                sens_and_city.append(sens_city.end_node["name"])
                print(sens_city)

            sens_and_meas_rel = self.gdb.match((None, sensor), r_type='WAS_MEASURED_BY')
            if len(sens_and_meas_rel) == 0:
                all_rows.append(sens_and_city)

            for measure_sens in sens_and_meas_rel:
                measure = measure_sens.nodes[0]

                whole_row = []
                whole_row.extend(sens_and_city)
                whole_row.append(measure["value"])
                whole_row.append(measure["time"])
                print(measure_sens)

                meas_parameter_rel = self.gdb.match((measure,), r_type='REPRESENTS')
                for param in meas_parameter_rel:
                    print(param)
                    whole_row.append(param.end_node["name"])
                all_rows.append(whole_row)

            table.extend(all_rows)

        print(table)
        return table

    def get_sens_params(self, sensor):
        sensor = self.gdb.nodes.match("Sensor", name=sensor).first()
        print(sensor)
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
            print(sensor)

            sens_and_city.append(sensor['name'])
            relations = self.gdb.match((sensor,), r_type='IS_PLACED_IN')
            for sens_city in relations:
                sens_and_city.append(sens_city.end_node["name"])
                print(sens_city)

            relations = self.gdb.match((None, sensor), r_type='WAS_MEASURED_BY')
            if len(relations) == 0:
                all_rows.append(sens_and_city)

            for measure_sens in relations:
                measure = measure_sens.nodes[0]

                whole_row = []
                whole_row.extend(sens_and_city)
                whole_row.append(measure["value"])
                whole_row.append(measure["time"])
                print(measure_sens)

                parameter = self.gdb.match((measure,), r_type='REPRESENTS')
                for param in parameter:
                    print(param)
                    whole_row.append(param.end_node["name"])
                all_rows.append(whole_row)

            table.extend(all_rows)

        print(table)
        return table

    def insert(self, new_request):
        time = str(datetime.now().hour) + ':' + str(datetime.now().minute)
        node = Node(VALUE, value=new_request[VALUE], time=time)
        print(node)
        sensor = self.get_node(SENSOR, new_request[SENSOR])
        print(sensor)
        param = self.get_node(PARAMETER, new_request[PARAMETER])
        print(param)

        node_sensor = Relationship(node, "WAS_MEASURED_BY", sensor)
        node_param = Relationship(node, "REPRESENTS", param)
        print(node_sensor, node_param)
        self.gdb.create(node_sensor)
        self.gdb.create(node_param)
