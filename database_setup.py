import database as db
import station_names
import process_data
import get_data
import os

# set up connection to the database
# edit this when working on the server
db.set_up_connection(db.db, 'weather')

# insert stations
stations_df = station_names.get_stations_dataframe()
db.insert_into_table(stations_df, 'Station')

# get daily measurement data
userpath = os.path.dirname(os.path.realpath(__file__))
#get_data.get_data(userpath, historical=True, recent=True,
#                  hourly=False, verbose=True)

# insert measurement data
print('inserting measurement data into the database...')
for i, s_id in enumerate(stations_df.index):
    try:
        mes = process_data.process_data(userpath, s_id, 'daily')
    except BaseException as e:
        print('something went wrong processing station: {}'.format(s_id))
        print(e)
    else:
        db.insert_into_table(mes, 'DailyMeasurement')
        print('{}: {}'.format(i, s_id))
