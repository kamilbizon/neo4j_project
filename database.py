import sqlite3 as lite
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd



def _create_and_return_greeting(tx, message):
    result = tx.run("CREATE (a:Greeting) "
                    "SET a.message = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=message)
    return result.single()[0]


class Database:
    def __init__(self, connect):
        try:
            self.gdb = Graph(auth=('neo4j', 'Passw0rd'))
            self.matcher = NodeMatcher(self.gdb)

            self.conn = lite.connect(connect, check_same_thread=False)
            self.cur = self.conn.cursor()
            print("connected to " + connect)

            print(self.gdb)
            self.get_all_measurements()
        except lite.Error as e:
            print('error: ' + str(e))
            exit()

    def get_all_measurements(self):
        sensors = list(self.matcher.match("Sensor"))
        for s in sensors:
            print(s)

    def select_table(self, table, where):
        sql = "SELECT * FROM " + table
        if where:
            sql += " WHERE " + where
        sql += ";"

        print(sql)

        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.conn.commit()
        except lite.Error as e:
            return str(e)

        return result

    def get_table(self, table, where=""):
        rows = self.select_table(table, where)

        result = "<table>"

        names = [description[0] for description in self.cur.description]
        result += "<tr>"
        for name in names:
            result += "<th>" + name + "</th>"
        result += "</tr>"

        for row in rows:
            result += "<tr>"
            for item in row:
                result += "<td>" + str(item) + "</td>"
            result += "</tr>"

        result += "</table>"

        return result

    def insert_row(self, table, col_data):
        node1 = Node("Sensor", name="sensor1")
        node2 = Node("Parameter", name="temp", value="15.0")
        relation = Relationship(node1, "MEASURES", node2)
        self.gdb.create(relation)

        sql = "INSERT INTO " + table

        sql += " ("
        for key in col_data:
            sql += key + ", "
        sql = sql[:-2]
        ###
        sql += ", data"
        ###
        sql += ") "

        sql += " VALUES ("
        for key in col_data:
            sql += '"' + str(col_data[key]) + '", '
        sql = sql[:-2]
        ###
        sql += ", datetime('now')"
        ###
        sql += ")"
        sql += ";"
        print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except lite.Error as e:
            return 'error: ' + str(e)

        return "dodano"

    def delete_row(self, table, where):
        exist = self.select_table(table, where)
        print(exist)
        if not exist:
            return "notatka nie istnieje"

        sql = "DELETE FROM " + table
        sql += " WHERE " + where
        sql += ";"

        print(sql)

        try:
            self.cur.execute(sql)
            self.conn.commit()
        except lite.Error as e:
            return 'error: ' + str(e)

        return "usunięto"

    def update_row(self, table, col_data, where):
        exist = self.select_table(table, where)
        if not exist:
            return "notatka nie istnieje"

        sql = "UPDATE " + table
        sql += " SET "
        for key in col_data:
            sql += key + " = '" + col_data[key] + "', "
        sql = sql[:-2]

        sql += " WHERE " + where
        sql += ";"

        print(sql)

        try:
            self.cur.execute(sql)
            self.conn.commit()
        except lite.Error as e:
            return 'error: ' + str(e)

        return "zaktualizowano"
