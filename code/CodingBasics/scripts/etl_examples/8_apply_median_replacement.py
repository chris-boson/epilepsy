from scratch_load_data import load_person_data
import pandas as pd
seizure_data_file_path = "/home/rob/Projects/epilepsy/code/CodingBasics/dummy_data/seizure_data.csv"
df_metadata = load_person_data()
seizure_data = pd.read_csv(seizure_data_file_path)
seizure_data = seizure_data.merge(df_metadata, on="patient_id", how="left")
#TODO ---------------- delete everything above this line

# If we want to replace the missing values in a column with the median of the values in that column,
# we need to do two things.

#First, we must gather all of the rows where the value is not missing
na_rows = seizure_data["iea_lead1"].isna()

#Notice we can just pass a column to the resultant indexed dataframe
iea_lead1_median = seizure_data[~na_rows]["iea_lead1"].median()

#Now we simply apply this value using the same indexes
seizure_data["iea_lead1"] = seizure_data["iea_lead1"].fillna(iea_lead1_median)

#We can also do other functions, such as replacing with the mean, and doing it in place. The pandas dicumentation is very rich.
#Here are the above steps as a one-liner
seizure_data["iea_lead1"].fillna(seizure_data[~na_rows]["iea_lead1"].mean(), inplace=True)