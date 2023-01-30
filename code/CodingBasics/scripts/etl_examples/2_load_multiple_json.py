import pandas as pd
import os

data_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/person_data"

#TODO ---------------- delete everything above this line

#The pattern is the same for json files, using pandas read_json function
#If we are concerned about memory, we can concatenate the dataframes on the fly as we read them

df_metadata = None
for parent_dir, subdirs, file_names in os.walk(data_path):

    #at each directory level, get a list of any csv files
    csv_file_names= [f for f in file_names if f.endswith(".json")]

    #create a full file path using the parent dir and the filename
    for csv_file_name in csv_file_names:
        file_path = os.path.join(parent_dir, csv_file_name)

        #read each file separately. json files should have their values in a list, otherwise you will need to use the 'typ' argument
        df = pd.read_json(file_path)

        #concat the original dataframe every time, except the very first time we read it, in which case we simply create a copy of it
        df_metadata = df if df_metadata is None else pd.concat([df_metadata, df])

#Finally we reset the index as before as it would have been very repetitive to do so every time 
df_metadata = df_metadata.reset_index(drop=True)

#We can now examine the dataframe with the head() argument, passing in the maximum number of rows we wish to preview
print(df_metadata.head(5))