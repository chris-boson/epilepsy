import pandas as pd
import os

#Initialize all the required paths
data_path = "/Users/ev105g/Documents/temp/epilepsy_book/R_chapter/data/"
data_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/person_data" #TODO - delete this
single_patient_folder = "D_EU/"
single_patient_folder = "personA" #TODO - delete this
filename = "metadata.csv"

#Concatenate the directories into a single file path
file_path = os.path.join(data_path, single_patient_folder, filename)

#Read in the csv file for a single patient
metadata_patient = pd.read_csv(file_path, sep=",")