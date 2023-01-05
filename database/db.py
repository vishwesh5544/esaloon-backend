import mysql.connector


class Db:
    _host = "127.0.0.1"
    _user = "root"
    _password = ""
    _database = "esaloon"
    _port = "3306"

    def __init__(self):
        self.connection = mysql.connector.connect(host=self._host, user=self._user, password=self._password, database=self._database,
                                                  port=self._port)
        self.cursor = self.connection.cursor(dictionary=True, buffered=True)
