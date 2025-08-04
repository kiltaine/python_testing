
import pandas as pd
import numpy as np
import os

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
print(flights[flights['ORIGIN'] == 'RNO'])
#print(pd.unique(flights['DAY_OF_WEEK'].sort_values(ascending=False)))
