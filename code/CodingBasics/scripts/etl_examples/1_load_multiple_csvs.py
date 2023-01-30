import pandas as pd
import os

#Initialize all the required paths
data_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/person_data" #TODO - delete this
patient_list = ["personA", "personB", "personC"] #TODO - delete this
filename = "metadata.csv" #TODO - delete this

#TODO ---------------- delete everything above this line

dfs = []
for patient_folder in patient_list:

    #Concatenate the directories into a single file path
    file_path = file_path = os.path.join(data_path, patient_folder, filename)
    
    #Read the single patient dataframe
    df = pd.read_csv(file_path, delimiter=",")

    #add it to the running list of dataframes
    dfs.append(df)

#We can create a single dataframe from a list of dataframes easily in pandas.
#The call to reset_index call will make sure our dataframe indexes rows correctly, starting from 0 and incrementing
df_metadata = pd.concat(dfs).reset_index(drop=True)


# Alternatively, we can rely on the os module to recursively crawl through the directory and read each csv file separately
dfs = []
for parent_dir, subdirs, file_names in os.walk(data_path):

    #at each directory level, get a list of any csv files
    csv_file_names= [f for f in file_names if f.endswith(".csv")]

    #create a full file path using the parent dir and the filename
    for csv_file_name in csv_file_names:
        file_path = os.path.join(parent_dir, csv_file_name)

        #read each file separately
        df = pd.read_csv(file_path)
        dfs.append(df)

df_metadata = pd.concat(dfs).reset_index(drop=True)


#If we are concerned about memory, we can concatenate the dataframes on the fly as we read them
df_metadata = None
for parent_dir, subdirs, file_names in os.walk(data_path):

    #at each directory level, get a list of any csv files
    csv_file_names= [f for f in file_names if f.endswith(".csv")]

    #create a full file path using the parent dir and the filename
    for csv_file_name in csv_file_names:
        file_path = os.path.join(parent_dir, csv_file_name)

        #read each file separately
        df = pd.read_csv(file_path)

        #concat the original dataframe every time, except the very first time we read it, in which case we simply create a copy of it
        df_metadata = df if df_metadata is None else pd.concat([df_metadata, df])

#Finally we reset the index as before as it would have been very repetitive to do so every time 
df_metadata = df_metadata.reset_index(drop=True)


#We can now examine the dataframe with the head() argument, passing in the maximum number of rows we wish to preview
print(df_metadata.head(5))