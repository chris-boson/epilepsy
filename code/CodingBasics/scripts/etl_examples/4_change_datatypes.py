from scratch_load_data import load_person_data
import pandas as pd

df_metadata = load_person_data()

#TODO ---------------- delete everything above this line

# Sometimes we may wish to convert a datatype to another
# This is often the case when string data is loaded that needs to be an integer
# Consult the pandas documentation for information on datatypes
df_metadata["patient_id"] = df_metadata["patient_id"].astype("int32")