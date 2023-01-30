from scratch_load_data import load_person_data
import pandas as pd

seizure_data_file_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/seizure_data.csv" #TODO - change this

df_metadata = load_person_data()

#TODO ---------------- delete everything above this line

seizure_data = pd.read_csv(seizure_data_file_path)

#We have two dataframes that are loaded, but we would like to merge them together.
#The patient id is the common column between the dataframes, and acts as the primary key on the metadata dataframe.
#The patient id column is the foreign key on the seizure dataframe
#Finally, we do a left join because we are interested in all rows of seizure data, regardless of whether or not they have a patient id in the metadata dataframe
seizure_data = seizure_data.merge(df_metadata, on="patient_id", how="left")

