from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year(s.datetime)) as year
                from new_ufo_sightings.sighting s 
                order by year DESC """

        cursor.execute(query, )

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(s.shape)
                from new_ufo_sightings.sighting s """

        cursor.execute(query, )

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from new_ufo_sightings.state s  """

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
        query = """select *
                from new_ufo_sightings.neighbor n """

        cursor.execute(query, )

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(s1, anno, forma):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select s.state, year(s.`datetime`), s.shape,count(s.id) as peso
                from new_ufo_sightings.sighting s
                where s.state = %s and year(s.`datetime`) = %s and s.shape = %s
                group by s.state, year(s.`datetime`), s.shape"""

        cursor.execute(query, (s1, anno, forma))

        for row in cursor:
            if row["peso"]:
                result = row["peso"]

        cursor.close()
        conn.close()
        return result