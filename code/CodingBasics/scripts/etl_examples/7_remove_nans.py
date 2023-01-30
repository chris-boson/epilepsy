from scratch_load_data import load_person_data
import pandas as pd

seizure_data_file_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/seizure_data.csv"
df_metadata = load_person_data()
seizure_data = pd.read_csv(seizure_data_file_path)
seizure_data = seizure_data.merge(df_metadata, on="patient_id", how="left")
#TODO ---------------- delete everything above this line

#In pandas, in many cases we will want to filter a dataframe. Dataframe filters act as true/false conditions on each
#row, and this vector of true's and falses are passed like indices to the dataframe to specify which rows are to be included

print(seizure_data.shape) #Original shape

na_rows = seizure_data["iea_lead1"].isna()
seizure_data = seizure_data[~na_rows]  #The '~' acts as a negation in pandas

print(seizure_data.shape) #Shape after filtering out nan rows