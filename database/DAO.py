from database.DB_connect import DBConnect
from model.location import Location


class DAO():

    @staticmethod
    def getAllProviders():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Provider 
                    FROM nyc_wifi_hotspot_locations
                    order by provider"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Provider"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllLocation(provider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT Location , AVG(Latitude) as Latitude  , AVG(Longitude) as Longitude 
                    from nyc_wifi_hotspot_locations
                    where provider = %s
                    group by Location 
                    """

        cursor.execute(query, (provider,))

        for row in cursor:
            result.append(Location(row["Location"], row["Latitude"], row["Longitude"] ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getLocationsDistance():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT Location ,AVG(Latitude) as Latitude  , AVG(Longitude) as Longitude 
                    from nyc_wifi_hotspot_locations
                    group by Location  """

        cursor.execute(query)

        for row in cursor:
            result[row["Location"]] = (row["Latitude"], row["Longitude"] )

        cursor.close()
        conn.close()
        return result
