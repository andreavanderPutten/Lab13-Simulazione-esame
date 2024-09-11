from database.DB_connect import DBConnect
from model.Stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime`) as anno
from new_ufo_sightings.sighting s 
order by anno desc"""

        cursor.execute(query, )

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape as forma
from new_ufo_sightings.sighting s 
where year(s.`datetime`)  = %s"""

        cursor.execute(query,(anno,) )

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
from new_ufo_sightings.state s"""

        cursor.execute(query, )

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getVicini():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as stato1, n.state2 as stato2
from new_ufo_sightings.neighbor n """

        cursor.execute(query, )

        for row in cursor:
            result.append((row["stato1"],row["stato2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(anno,forma,stato1,stato2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct s.id) + count(distinct s2.id) as peso 
from new_ufo_sightings.sighting s, new_ufo_sightings.sighting s2 
where s.shape = %s 
and year(s.`datetime`) = %s
and year(s2.`datetime`) = %s
and s2.shape = %s
and s.state = %s
and s2.state = %s"""

        cursor.execute(query,(forma,anno,anno,forma,stato1,stato2))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result