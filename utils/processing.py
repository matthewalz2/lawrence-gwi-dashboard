from utils.data_loader import read_csv_fallback

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
    data = data.rename(columns={'Unnamed: 0': 'Categories', 
                                'Lawrence city, Massachusetts':'Estimate',
                                'Unnamed: 2': 'Margin of Error'})

    data['Categories'] = data['Categories'].str.strip(':')
    housing = data.drop(data.index[0])
    return housing

def clean_age_sex_data_m(data):
    data = data[2:25]
    data = data.rename(columns={'Group': 'Age Group'})
    return data

def clean_age_sex_data_f(data):
    data = data[26:]
    data = data.rename(columns={'Group': 'Age Group'})
    return data

print(clean_race_data_mixed(df1))
