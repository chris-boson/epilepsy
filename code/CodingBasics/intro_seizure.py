# Import necessary libraries
import json
import os
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Define data path
data_path = "./patient_data/"
output_dir = "./outputs/"
single_patient_folder = "Patient_1/"
filename = "metadata.csv"

# Concatenate all directories (as strings)
file_path = os.path.join(data_path, single_patient_folder, filename)

# Read in the csv file for a single patient
metadata_patient1 = pd.read_csv(file_path)

# Initialize a list with all patient's folders x
patients_list = ["Patient_{}".format(i) for i in range(1, 21)]

# Initialize the DataFrame where the patient's metadata and seizure data will be stored
df_metadata = pd.DataFrame()
seizure_data = pd.DataFrame()

# Get the metadata, seizure data, and time data for all patients
for patient in patients_list:
    # Get the filepaths for each patient
    metadata_filepath = os.path.join(data_path, patient, "metadata.csv")
    seizure_filepath = os.path.join(data_path, patient, "sdata.json")
    time_filepath = os.path.join(data_path, patient, "timedata.mat")

    # Load the patient's metadata
    metadata_current_patient = pd.read_csv(metadata_filepath)

    # Concatenate the metadata dataframes
    df_metadata = pd.concat([df_metadata, metadata_current_patient], ignore_index=True)

    # Load json seizure data
    with open(seizure_filepath) as f:
        seizure_current_patient = json.loads(json.load(f)[0])
    seizure_current_patient_df = pd.json_normalize(seizure_current_patient)

    # Concatenate the seizure data dataframes
    seizure_data = pd.concat([seizure_data, seizure_current_patient_df], ignore_index=True)

    # Load and convert timedata to timestamp
    mat = scipy.io.loadmat(time_filepath)
    timedata = pd.to_datetime(
        mat["time_stamps"].ravel(), format="%Y-%m-%d %H:%M:%S", errors="coerce"
    )

    # Assign the timestamps to the correct rows in seizure_data dataframe
    seizure_data.loc[
        seizure_data["patient_id"] == int(patient.split("_")[1]), "hourly_markers"
    ] = timedata

# Convert patient_id to match format in metadata
seizure_data["patient_id"] = "Patient_" + seizure_data["patient_id"].astype(str)

# Join the metadata into the dataframe
seizure_data = pd.merge(seizure_data, df_metadata, left_on="patient_id", right_on="ID", how="left")

# Convert age and patient_id columns from strings to integers
seizure_data["Age"] = seizure_data["Age"].astype(int)

# Convert all column names to lower case
seizure_data.columns = [c.lower() for c in seizure_data.columns]

# Replace 'FALSE' with 'F' in the gender column
seizure_data["gender"] = seizure_data["gender"].replace("FALSE", "F")

# Rename columns
seizure_data.rename(columns={"na.": "first_visit_date"}, inplace=True)

# Check unique values for potential missing values
print(seizure_data["na..1"].unique())

# Drop the column with missing values
seizure_data = seizure_data.drop(columns=["na..1"])

# Print column names
print(seizure_data.columns)


# Define a function for displaying all columns that have NA
def display_na(df, threshold):
    na_percent_per_column = df.isna().mean().round(3)
    return na_percent_per_column[na_percent_per_column > threshold]


# If NA is present in any row of the entire dataframe drop that row
any_na_drop = seizure_data.dropna()

# Complete case removal
partial_na_drop = seizure_data[seizure_data.iloc[:, 1:2].notna().all(axis=1)]

# Impute with median
for col in seizure_data.columns:
    if seizure_data[col].dtype == "object":  # if column is categorical or string
        seizure_data[col] = seizure_data[col].fillna("unknown")
    else:  # if column is numerical
        seizure_data[col] = seizure_data[col].fillna(seizure_data[col].median())

# Check again to make sure that there are no NA
display_na(seizure_data, 0.01)

# Add the two leads and use the aggregated variable. Drop the individual ones
seizure_data["iea_lead_agg"] = seizure_data["iea_lead1"] + seizure_data["iea_lead2"]
seizure_data.drop(["iea_lead1", "iea_lead2"], axis=1, inplace=True)

# Built a histogram to explore the data - it looks like the majority of the seizure counts are
# near 0. We have a very left skewed histogram with very few observations having >10 seizures.
# Contributing to this may be the fact that each observation represents the number of seizures
# within a 1 hour window
Path("./outputs").mkdir(parents=True, exist_ok=True)

plt.hist(seizure_data["le"], bins=50, density=True)
plt.xlabel("Seizures")
plt.ylabel("Density")
plt.savefig("./outputs/le_histogram.png")
plt.clf()

plt.hist(seizure_data["iea_lead_agg"], bins=50, density=True)
plt.xlabel("Seizure Spikes")
plt.ylabel("Density")
plt.savefig("./outputs/iea_lead_agg.png")
plt.clf()

# An alternative way to look at the seizure counts is to use summary - A quick look confirms what
# we observed via the histogram - most seizures within a 1 hour interval are 0. In fact even the
# 3rd quartile is 0 indicating that 75% of the observations have 0 seizures
print(seizure_data["iea_lead_agg"].describe())

# Extract the dates from the time stamps
seizure_data["seizure_date"] = seizure_data["hourly_markers"].dt.date

# Aggregate the seizures and spikes on daily level into a new dataframe
daily_seizures_spikes = (
    seizure_data.groupby(["patient_id", "seizure_date"])
    .agg(
        total_le=pd.NamedAgg(column="le", aggfunc="sum"),
        total_iea_lead_agg=pd.NamedAgg(column="iea_lead_agg", aggfunc="sum"),
    )
    .reset_index()
)

plt.hist(daily_seizures_spikes["total_le"], bins=50, density=True)
plt.xlabel("Seizures")
plt.ylabel("Density")
plt.savefig("./outputs/daily_le_histogram.png")
plt.clf()

plt.hist(daily_seizures_spikes["total_iea_lead_agg"], bins=50, density=True)
plt.xlabel("Seizure Spikes")
plt.ylabel("Density")
plt.savefig("./outputs/daily_iea_lead_agg.png")
plt.clf()


# An alternative way to look at the seizure counts is to use summary - A quick look confirms what
# we observed via the histogram - most seizures within a 1 hour interval are 0. In fact even the
# 3rd quartile is 0 indicating that 75% of the observations have 0 seizures
print(seizure_data["iea_lead_agg"].describe())

# Extract the dates from the time stamps
seizure_data["seizure_date"] = pd.to_datetime(seizure_data["hourly_markers"]).dt.date

# Aggregate the seizures and spikes on daily level into a new dataframe
daily_seizures_spikes = (
    seizure_data.groupby(["patient_id", "seizure_date"])
    .agg(
        total_le=pd.NamedAgg(column="le", aggfunc="sum"),
        total_iea_lead_agg=pd.NamedAgg(column="iea_lead_agg", aggfunc="sum"),
    )
    .reset_index()
)

plt.hist(daily_seizures_spikes["total_le"], bins=50, density=True)
plt.xlabel("Seizures")
plt.ylabel("Density")
plt.savefig("./outputs/daily_le_histogram.png")
plt.clf()

plt.hist(daily_seizures_spikes["total_iea_lead_agg"], bins=50, density=True)
plt.xlabel("Seizure Spikes")
plt.ylabel("Density")
plt.savefig("./outputs/daily_iea_lead_agg.png")
plt.clf()

# Look at the unique seizure focus values - there are 5
print(seizure_data["seizure_foci"].unique())

# Does each patient have each of the seizure foci - it looks like the seizure_focus is unique to
# each patient.
print(seizure_data.groupby("patient_id")["seizure_foci"].nunique())

# Display all the patients that correspond to each seziure focus
print(seizure_data.groupby("seizure_foci")["patient_id"].unique())

# Convert the gender and seizure foci columns to category
seizure_data[["gender", "seizure_foci"]] = seizure_data[["gender", "seizure_foci"]].astype(
    "category"
)

# Let's explore the time series component of the data
print(seizure_data["hourly_markers"].min())
print(seizure_data["hourly_markers"].max())
print(seizure_data["hourly_markers"].nunique())

# Do all patients have the same number of datapoints?
print(seizure_data.groupby("patient_id")["hourly_markers"].nunique())

# Drop duplicate observations
seizure_data.drop_duplicates(inplace=True)

# Patient 6
seizure_data_2017_patient_6 = seizure_data[seizure_data["patient_id"] == "Patient_6"]

# Let's plot the time series of the spikes; since the data is quite large and we have a lot of zeros we will just explore data between February 1st, 2017 and March 20th, 2017. We pick these time periods as they contain seizures and this can be useful for our later analysis
mask = (seizure_data_2017_patient_6["hourly_markers"] > pd.Timestamp("2017-02-01")) & (
    seizure_data_2017_patient_6["hourly_markers"] <= pd.Timestamp("2017-03-20")
)
seizure_data_subset_2017_patient_6 = seizure_data_2017_patient_6.loc[mask]

fig, ax = plt.subplots()

# Create a plot for the spikes
ax.plot(
    seizure_data_subset_2017_patient_6["hourly_markers"],
    seizure_data_subset_2017_patient_6["iea_lead_agg"],
    label="Spikes",
)

# Add the seizures as dots to the plot; it looks like a lot of the seizures are occurring on the upward cycle of a spike
seizure_subset = seizure_data_subset_2017_patient_6[seizure_data_subset_2017_patient_6["le"] > 0]
ax.scatter(
    seizure_subset["hourly_markers"], seizure_subset["iea_lead_agg"], color="red", label="Seizures"
)

ax.set_xlabel("Date")
ax.set_ylabel("Spikes")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.legend()
plt.savefig("./outputs/hourly_seizure_spikes.png")
plt.clf()
