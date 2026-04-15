from utils.data_loader import read_csv_fallback
import pandas as pd

df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')

def clean_race_data_single(data):
    #Strip label column from any punctuation/white space
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip()
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip(':')

    #Rename my columns
    data = data.rename(columns={'Label (Grouping)': 'Race',
                                'Lawrence city, Massachusetts!!Estimate' : 'Resident Count'
})

    #Filter to single race values
    single_race = data[1:7]

    return single_race

def clean_race_data_mixed(data):
    #Strip label column from any punctuation/white space
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip()
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip(':')

    #Rename my columns
    data = data.rename(columns={'Label (Grouping)': 'Race',
                                'Lawrence city, Massachusetts!!Estimate' : 'Resident Count'})
    
    #Filter for mixed race rows
    mixed_race = data[7:]
    return mixed_race

def clean_housing_data(data):
    data.columns = data.columns.str.strip()

    data = data.rename(columns={
        data.columns[0]: 'Categories',
        data.columns[1]: 'Estimate',
        data.columns[2]: 'Margin of Error'
    })

    # Clean text
    data['Categories'] = data['Categories'].str.strip(':').str.strip()

    # Clean numbers
    data['Estimate'] = data['Estimate'].replace({',': ''}, regex=True)
    data['Estimate'] = pd.to_numeric(data['Estimate'], errors='coerce')

    # drop bad rows
    data = data[~data['Categories'].isin(['Label', 'Total'])]

    # Keep only what we need
    data = data[['Categories', 'Estimate']].copy()
    unknown = pd.DataFrame({'Categories': ['Unknown'], 'Estimate': [89332 - data['Estimate'].sum()]})
    data = pd.concat([data, unknown], ignore_index=True)

    return data

def clean_age_sex_data(data):
    # Rename columns
    data = data.rename(columns={
        data.columns[0]: "Age Group",
        data.columns[1]: "Estimate"
    })

    # Clean numeric column
    data["Estimate"] = data["Estimate"].replace({",": ""}, regex=True)
    data["Estimate"] = data["Estimate"].astype(int)

    # Split male and female sections
    male = data[2:25][["Age Group", "Estimate"]].copy()
    female = data[26:][["Age Group", "Estimate"]].copy()

    # Add gender labels
    male["Gender"] = "Male"
    female["Gender"] = "Female"

    # Combine into one dataset (THIS is the key change)
    combined = pd.concat([male, female], axis=0)

    return combined

