import pandas as pd
import numpy as np

flights = pd.read_csv('flights.csv', index_col=False)
flights['FL_DATE'] = pd.to_datetime(flights['FL_DATE'])
flights[['CANCELLED','DIVERTED']] = flights[['CANCELLED','DIVERTED']].astype(bool)

flight_test = flights[['CANCELLED','DIVERTED']]

#print(flight_test[(flight_test['CANCELLED'] == True) & (flight_test['DIVERTED'] == True)])

#remove first three columns
flights.drop(columns=['YEAR', 'MONTH', 'DAY_OF_MONTH'],inplace=True)
flights.rename(columns={'DEST':'DESTINATION'}, inplace=True)

#flights.dropna(inplace=True)

flight_null = pd.DataFrame(flights['DEP_TIME'])
#print(flight_null)
nulls = pd.DataFrame(flight_null['DEP_TIME'].fillna('toto je null'))
nulls = nulls[nulls['DEP_TIME'] == 'toto je null']

print(nulls)




        
#print(flights.isnull().sum())