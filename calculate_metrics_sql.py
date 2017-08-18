import pandas as pd
import numpy as np
from pandasql import *

pysqldf = lambda q: sqldf(q, globals())

# load google places data
google_data = pd.read_excel("google.xlsx")    #, index_col = 0
#google_data = pd.ExcelFile("google.xlsx")
google_data['loc_lat'] = list(map(float, google_data['loc_lat'].str.replace(",", ".")))
google_data['loc_lng'] = list(map(float, google_data['loc_lng'].str.replace(",", ".")))
google_data['rating'] = list(map(float, google_data['rating'].str.replace(",", ".")))
google_data['rid'] = google_data.index.get_values()

google_data['name'].str.lower()
google_data['types'].str.lower()
# get McDonalds and similar by types list places
mc_data = google_data[(google_data['name'].str.contains("mcdon", na = False)) |
                            (google_data['types'] == "restaurant, food, point_of_interest, establishment")]

q = """
SELECT
    m.*,
    a.*
FROM
    record m
            LEFT JOIN google_data a ON  m.types != a.types
                                    and m.num_rec != a.num_rec
                                    and m.loc_lat <= a.loc_lat + 0.012
                                    and m.loc_lat >= a.loc_lat - 0.012
                                    and m.loc_lng <= a.loc_lng + 0.025
                                    and m.loc_lng >= a.loc_lng - 0.025                                    
"""

df_all = pd.DataFrame()
#pd.concat(df_all, df)
#new_df = pysqldf(q)
for i in range(len(mc_data)):
    #record =  pd.DataFrame(mc_data.iloc[i,:].values)
    record = mc_data.iloc[[i]]
    #record.columns = mc_data.columns
    fd_for = pysqldf(q)
    df_all = pd.concat([df_all, fd_for])
    print(len(df_all))

df_all