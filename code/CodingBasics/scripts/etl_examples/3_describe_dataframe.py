import pandas as pd
from scratch_load_data import load_person_data

df_metadata = load_person_data()

#TODO ---------------- delete everything above this line

#We can view the first n rows of the dataframe using the 'head' function
df_metadata.head(5)

#We can also view the datatypes of each column
print(df_metadata.dtypes)

