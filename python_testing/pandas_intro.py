
import pandas as pd
import numpy as np


df_data = {
    'col1' : np.random.rand(5),
    'col2' : np.random.rand(5),
    'col3' : np.random.rand(5)
}

df = pd.DataFrame(df_data)

#print(df[:2])
#print(df['col1'])

tracks = pd.read_excel('Course Files/Tracks.xls', sheet_name=0)


flights = pd.read_csv('flights.csv',index_col = False)
flights_mini = flights[['ORIGIN', 'DEST']]
flight_to_csv = flights_mini[flights_mini['ORIGIN'] == 'RNO']
#print(pd.unique(flights['DAY_OF_WEEK'].sort_values(ascending=False)))


#print(flights.iloc[5,flights.columns.get_loc('ORIGIN')])
#print(flights.columns[1])

#print(flights.columns)


#pouze liché pozice v headru
array = []
for i in flights.columns:
    member = list(flights.columns).index(i)
    array.append(member)

array_odd = []
for j in array:
    if j%2 == 0:
        array_odd.append(j)


for k in array_odd:
    list_test = list(flights)[k]
    #print(list_test)

#jednodušší způsob + konverze do jednoho řádku s oddělovačem    
testing = ''    
for m in flights.columns[::2]:
    testing += m + ', '

testing = testing[:-2]


sorting = flights.sort_values(by=['DISTANCE','AIR_TIME'], ascending=False)


spec_flights = flights[(flights['DISTANCE']>4000) & ~(flights['MONTH'] == 1)]

flights_by_month = flights.groupby(['MONTH'])

print(flights_by_month['DISTANCE'].aggregate("sum"))
print(flights_by_month['DISTANCE'].aggregate("sum").min())
print(flights_by_month['DISTANCE'].aggregate("sum").idxmin())

