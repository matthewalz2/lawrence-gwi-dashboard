from utils.data_loader import read_csv_fallback
import pandas as pd
import re

df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')
df4 = read_csv_fallback('data/Lawrence GWI Education.csv')

def clean_race_data_single(data):
    #Strip label column from any punctuation/white space
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip()
    data['Label (Grouping)'] = data['Label (Grouping)'].str.strip(':')

    #Rename my columns
    data = data.rename(columns={'Label (Grouping)': 'Race',
                                'Lawrence city, Massachusetts!!Estimate' : 'Resident Count'
})

    #Filter to single race values
    race = data[1:8]

    return race


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

#This function allows us to create custom binning, just mapping labels to different first number values in preestablished labels. 

def bin_age_groups(df):
    df = df.copy()

    def map_bin(label):
        if "Under 5" in label:
            return "Under 5"
        if "5 to 9" in label or "5-9" in label:
            return "5–9"
        if "85" in label:
            return "85+"

        match = re.search(r'\d+', label)
        if not match:
            return label

        age = int(match.group())

        if 10 <= age <= 17:
            return "10–17"
        elif 18 <= age <= 24:
            return "18–24"
        elif 25 <= age <= 34:
            return "25–34"
        elif 35 <= age <= 44:
            return "35–44"
        elif 45 <= age <= 54:
            return "45–54"
        elif 55 <= age <= 64:
            return "55–64"
        elif 65 <= age <= 74:
            return "65–74"
        elif 75 <= age <= 84:
            return "75–84"
        else:
            return label

    df["Age Group"] = df["Age Group"].apply(map_bin)

    # group after mapping
    df = df.groupby(["Age Group", "Gender"], as_index=False)["Estimate"].sum()

    return df


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

    #apply our previous binning function
    male = bin_age_groups(male)
    female = bin_age_groups(female)

    # Combine into one dataset (THIS is the key change)
    combined = pd.concat([male, female], axis=0)

    return combined

'''Education will have two dataframes that need to be plotted, one will
   be for 18-24 year olds donut plot, one will be color coded bar chart 
   for 25+, colors are salary
'''
def clean_education_18_24(data):
  data.columns = data.columns.str.strip()

  #rename columns
  data = data.rename(columns={
        data.columns[0]: 'Groups',
        data.columns[1]: 'Estimate',
        data.columns[2]: 'Margin of Error',
        data.columns[3]: 'Percent Estimate',
        data.columns[4]: 'Percent Margin of Error'
  })

  #For overview, only need these columns for general population not gendered
  data = data[['Groups', 'Estimate', 'Margin of Error', 'Percent Estimate', 'Percent Margin of Error']]

  # clean all columns for special characters
  for col_name in data:
    data[col_name] = (
        data[col_name]
        .astype(str)
        .str.replace('\xa0', '', regex=True)
        .str.replace('Â', '', regex=True)
        .str.strip()
    )

  #drop first row
  data = data.drop(data.index[0])
  data = data.iloc[1:5]

  #strip estimate from commas and store as integer
  data['Estimate'] = (
        data['Estimate']
        .astype(str)
        .str.replace(',', '', regex=True)
        .astype(int)
    )

  return data



def clean_ed_earnings_25_plus(ed_data):
    # -----------------------------
    # CLEAN BASE DATA
    # -----------------------------
    ed_data.columns = ed_data.columns.str.strip()

    ed_data = ed_data.rename(columns={
        ed_data.columns[0]: 'Groups',
        ed_data.columns[1]: 'Estimate',
        ed_data.columns[2]: 'Margin of Error',
        ed_data.columns[3]: 'Percent Estimate',
        ed_data.columns[4]: 'Percent Margin of Error'
    })

    ed_data = ed_data[['Groups', 'Estimate', 'Margin of Error',
                       'Percent Estimate', 'Percent Margin of Error']]

    # Clean text
    ed_data['Groups'] = (
        ed_data['Groups']
        .astype(str)
        .str.replace('\xa0', '', regex=True)
        .str.replace('Â', '', regex=True)
        .str.strip()
    )

    # -----------------------------
    # 25+ EDUCATION DATA (7 rows)
    # -----------------------------
    ed_25_plus = ed_data.iloc[7:14].copy()

    ed_25_plus['Estimate'] = (
        ed_25_plus['Estimate']
        .astype(str)
        .str.replace(',', '', regex=True)
    )
    ed_25_plus['Estimate'] = pd.to_numeric(ed_25_plus['Estimate'], errors='coerce')

    # -----------------------------
    # EARNINGS DATA
    # -----------------------------
    earnings = ed_data.iloc[62:69].copy()

    earnings = earnings[['Groups', 'Estimate']]
    earnings = earnings.rename(columns={'Estimate': 'Estimated Salary'})

    earnings['Estimated Salary'] = (
        earnings['Estimated Salary']
        .astype(str)
        .str.replace(',', '', regex=True)
    )
    earnings['Estimated Salary'] = pd.to_numeric(earnings['Estimated Salary'], errors='coerce')

    # Drop aggregate row
    earnings = earnings.iloc[1:].copy()

    # Get correct base values
    base = earnings['Estimated Salary'].tolist()[1:]

    # Build EXACT correct structure
    salary_values = [
        38531,      # Less than 9th
        38531,      # 9–12
        base[0],    # HS → 39082
        base[1],    # Some college → 41079
        base[1],    # Associate's → 41079
        base[2],    # Bachelor's → 62026
        base[3]     # Graduate → 64186
    ]

    # Assign to dataframe
    ed_25_plus['Estimated Salary'] = salary_values

    # Return final cleaned dataframe
    return ed_25_plus










'''
Function to clean Employment data
'''
