# imports
import mysql.connector as mc
import pandas as pd
import requests
import json
import datetime

''' 
    main process , checking the relevancy of the various locations possible for corona test in the 
    vicinity of the user.
    the user is sending his location via telegram bot using normal address.
    the system will translate the address to coordinates using API then will compare the coordinates with the coordinates
    of the various possible locations and will return the closest one. then the system will check the load of 
    the corona locations and will return the place with less people attending.
    the system will translate the coordinates back to normal address.
    
    the system now will send back via the telegram bot the user the  address of this selected location.
    
    * there are several other processes running in different scripts
'''

# declaring class for selected result
class msg_Result:
    def __init__(self):
        print(1)

    # function will return coordinate that translated  using API
    def get_Response(Location):
        try:
            # API that translating address to coordinates
            url = f'http://xaviercat.com:8089/address?key=2021&address={Location}'
            response = requests.request("GET", url).json()
        except:
            response = {'lat': 99.9999999, 'lng': 99.9999999}
        print(f'"{url}"')
        return response

    # function will return the final target location
    def get_Location(Location):

        # creating connection to mysql
        mysql_conn = mc.connect(
            user='naya',
            password='naya',
            host='localhost',
            port=3306,
            autocommit=True,  # <--
            database='Cellular')

        # find the unix time 30 min back
        From_CallDateTime = datetime.datetime.now() - datetime.timedelta(days=17, hours=0, minutes=30)

        # df_CellularAntennas  = dataframe that holds the outcome of
        # calculation of the amount of people in the vicinity of the cellular antennas
        # in the last 30 minutes
        select_statement = """
           SELECT F.siteName, COUNT(*) as towerCount,Longitude,Latitude
           FROM Cellular.CallsData AS F
           LEFT JOIN Cellular.Dim_CellularAntennas_Stations AS A
           ON A.siteName = F.siteName
           WHERE callDuration > 60 
           AND CallDateTime >= '{From_CallDateTime}'
           GROUP BY F.siteName,Longitude,Latitude; """.format(From_CallDateTime=From_CallDateTime.strftime("%Y-%m-%d %H:%M:%S"))

        mysql_cursor = mysql_conn.cursor()
        df_CellularAntennas = pd.read_sql(select_statement, con=mysql_conn)

        print(df_CellularAntennas)

        ## this API will returm coordinates from street  address
        try:
            url = f'http://xaviercat.com:8089/address?key=2021&address={Location}'
            response = requests.request("GET", url).json()
        except:
            response = {'lat': 99.9999999, 'lng': 99.9999999}
        print(url)

        # this is the value of the distance of the user's address from the corona test locations
        # used in calculations ( 2 km )
        Factor = 0.020

        x = response["lat"]
        y = response["lng"]
        x=float(x)
        y=float(y)

        # df_CoronaCheck = dataframe that holds the locations of all
        # corona test stations in a distance of 2 km from the location of the user's address
        select_statement= """
           SELECT * FROM Cellular.Dim_CoronaCheck_Stations
           WHERE Latitude >= {x_min} and Latitude <= {x_max}
           AND  Longitude >= {y_min} and Longitude <= {y_max} ;
           """.format(x_min = x - Factor , x_max = x + Factor, y_min = y - Factor , y_max = y + Factor)

        df_CoronaCheck = pd.read_sql(select_statement , con=mysql_conn)

        # closing connection to mysql
        mysql_cursor.close()

        ############  df_result  ##################

        df_result = pd.DataFrame(columns=['Location', 'towerCount'])

        # this is the value used to calculate the max distance from corona test stations
        # we should look for antennas around
        # used in calculations ( 1 km )
        Factor = 0.010

        # passing the DF and selecting the antennas in 'factor" distance
        for index, row in df_CoronaCheck.iterrows():
            x_min = float(row['Latitude']) - float(Factor)
            x_max = float(row['Latitude']) + float(Factor)
            y_min = float(row['Longitude']) - float(Factor)
            y_max = float(row['Longitude']) + float(Factor)

            # filtering out the desired antennas
            df = df_CellularAntennas.where(pd.to_numeric(df_CellularAntennas["Latitude"]) >= x_min)
            df = df[df.siteName.notnull()]
            df = df[pd.to_numeric(df["Latitude"]) <= x_max]
            df = df[df["Longitude"] >= y_min]
            df = df[df["Longitude"] <= y_max]


            # API distance calculator
            distance = """&from={x1},{y1}&to={x2},{y2}""".format(x1=x,
                                                                                                                    y1=y,
                                                                                                                    x2=float(row["Latitude"]),
                                                                                                                    y2=float(row["Longitude"]))
            api = 'http://xaviercat.com:8093/distance?key=2021'
            url = api + distance
            print(url)
            data = requests.get(url)
            #  print(data.text)
            distance = json.loads(data.text)['distance']
            print('distance', distance)

            # adding a row with the distance of the user from each corona test location
            new_row = {'Location': row["Location"], \
                       'Latitude': row["Latitude"], \
                       'Longitude': row["Longitude"], \
                       'towerCount': int(df.sum(axis=0)[1]), \
                       'distance': distance}

            df_result = df_result.append(new_row, ignore_index=True)
            print('sum', df.towerCount)

        # debug: the result of the calculations
        print(f'df_result {df_result}')

        # returns the most close location, if there is none, will return 'invalid'.
        try:
            df = df_result.sort_values(by=['towerCount', 'distance']).head(1)['Location']
            for x in df:
                return x
        except:
                return 'invalid result'

