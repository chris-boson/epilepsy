from scratch_load_data import load_person_data
import pandas as pd
seizure_data_file_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/seizure_data.csv"
df_metadata = load_person_data()
seizure_data = pd.read_csv(seizure_data_file_path)
seizure_data = seizure_data.merge(df_metadata, on="patient_id", how="left")
#TODO ---------------- delete everything above this line

#In pandas, there are built-in functions that allow us to perform common transformations on data.
#One of these transformations is to replace null values. 
#Here we can replace all nan values in a column with a specified value

seizure_data["iea_lead1"] = seizure_data["iea_lead1"].fillna(0.1)
seizure_data["gender"] = seizure_data["gender"].astype("str")

#Let us fix the gender column by replacing instances of 'False' with 'F', as we have seen this in the data.

def replace_gender_value(val):
    if val.lower() == "false":
        return "F"
    return val

#We have to point the column at this transformation function using the 'apply' method
seizure_data["gender"] = seizure_data["gender"].apply(lambda x: replace_gender_value(x))