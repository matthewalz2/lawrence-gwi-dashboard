from utils.data_loader import read_csv_fallback
import pandas as pd
import re

'''====================================='''
#NEW FUNCTIONS BELOW
'''====================================='''

#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦DEMOGRAPHIC PROCESSING🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩
#Age and gender processing and sorting from census downloader
def age_gender_processing(demo_df):
    # Make a copy to avoid modifying the original DataFrame
    demo = demo_df.copy()

    # Drop specified rows
    demo = demo.drop(demo.index[[44, 45, 28]])
    demo = demo[5:51]

    # Organization of Male and Female Age Groups
    male_df = demo[demo['groups'].str.startswith('Male: ')].copy()
    female_df = demo[demo['groups'].str.startswith('Female: ')].copy()

    male_df['age_group'] = male_df['groups'].str.replace('Male: ', '')
    female_df['age_group'] = female_df['groups'].str.replace('Female: ', '')

    male_df = male_df.rename(columns={'values': 'male_count'})
    female_df = female_df.rename(columns={'values': 'female_count'})

    demographics_df = pd.merge(male_df[['age_group', 'male_count']], female_df[['age_group', 'female_count']], on='age_group', how='outer')

    demographics_df['total'] = demographics_df['male_count'] + demographics_df['female_count']

    demographics_df = demographics_df[['age_group', 'male_count', 'female_count', 'total']]

    # Original custom binning function (nested within or defined before if preferred)
    def bin_age_groups(df):
        df = df.copy()

        def map_bin(label):
            if 'Under 5' in label:
                return 'Under 5'
            if '5 to 9' in label or '5-9' in label or '5–9' in label:
                return '5–9'
            if '85' in label:
                return '85+'

            match = re.search(r'\d+', label)
            if not match:
                return label

            age = int(match.group())

            if 10 <= age <= 17:
                return '10–17'
            elif 18 <= age <= 24:
                return '18–24'
            elif 25 <= age <= 34:
                return '25–34'
            elif 35 <= age <= 44:
                return '35–44'
            elif 45 <= age <= 54:
                return '45–54'
            elif 55 <= age <= 64:
                return '55–64'
            elif 65 <= age <= 74:
                return '65–74'
            elif 75 <= age <= 84:
                return '75–84'
            else:
                return label

        df['Age Group'] = df['Age Group'].apply(map_bin)

        # group after mapping
        df = df.groupby(['Age Group', 'Gender'], as_index=False)['Estimate'].sum()

        return df

    # Melt the demographics_df to create 'Gender' and 'Estimate' columns
    demographics_melted = demographics_df.melt(
        id_vars=['age_group'],
        value_vars=['male_count', 'female_count'],
        var_name='Gender',
        value_name='Estimate'
    )

    # Rename 'age_group' to 'Age Group' to match the function's expectation
    demographics_melted = demographics_melted.rename(columns={'age_group': 'Age Group'})

    # Map 'male_count' to 'Male' and 'female_count' to 'Female'
    demographics_melted['Gender'] = demographics_melted['Gender'].replace({
        'male_count': 'Male',
        'female_count': 'Female'
    })

    # Apply the binning function
    binned_demographics_melted = bin_age_groups(demographics_melted)

    # Pivot the binned_demographics_melted back to the desired format
    binned_demographics_df = binned_demographics_melted.pivot_table(
        index='Age Group',
        columns='Gender',
        values='Estimate',
        fill_value=0
    ).reset_index()

    binned_demographics_df.columns.name = None # Remove the 'Gender' column name from index

    # Rename columns to match the requested output
    binned_demographics_df = binned_demographics_df.rename(columns={
        'Male': 'male_count',
        'Female': 'female_count'
    })

    # Calculate the total
    binned_demographics_df['total'] = binned_demographics_df['male_count'] + binned_demographics_df['female_count']

    # Reorder columns
    binned_demographics_df = binned_demographics_df[['Age Group', 'male_count', 'female_count', 'total']]

    # Proper order of the categories
    age_group_order = [
        'Under 5',
        '5–9',
        '10–17',
        '18–24',
        '25–34',
        '35–44',
        '45–54',
        '55–64',
        '65–74',
        '75–84',
        '85+'
    ]

    print("Unique Age Groups before Categorical conversion:")
    print(binned_demographics_df['Age Group'].unique())

    binned_demographics_df['Age Group'] = pd.Categorical(binned_demographics_df['Age Group'], categories=age_group_order, ordered=True)

    sorted_age_gender_df = binned_demographics_df.sort_values('Age Group').reset_index(drop=True)

    return sorted_age_gender_df


#General Race Distribution (Almost identical to first iteration)
def demo_race_processing(demo_df):
  race = demo_df[55:61].copy()
  return race

#HISPANIC POPULATION (May be interesting if the population is dominant with other race, at least since Lawrence is)
def demo_hispanic_processing(demo_df):
    hispanic = demo_df[81:111].copy()

    # Remove summary rows
    hispanic = hispanic[
        ~hispanic["groups"].isin([
            "Total (citizenship universe)",
            "Hispanic or Latino"
        ])
    ]

    hispanic["values"] = pd.to_numeric(
        hispanic["values"],
        errors="coerce"
    )

    threshold = 1000

    # Combine small groups and the existing "All other Hispanic or Latino"
    hispanic["group"] = hispanic.apply(
        lambda row: (
            "Other"
            if (
                row["values"] < threshold
                or row["groups"] == "All other Hispanic or Latino"
            )
            else row["groups"]
        ),
        axis=1
    )

    hispanic = (
        hispanic.groupby("group", as_index=False)["values"]
        .sum()
    )

    # Force Other to the bottom
    hispanic["sort"] = hispanic["group"].eq("Other")

    hispanic = (
        hispanic.sort_values(
            ["sort", "values"],
            ascending=[True, False]
        )
        .drop(columns="sort")
        .reset_index(drop=True)
    )

    return hispanic







#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦EDUCATION PROCESSING🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩
def edu_attainment_processing(edu_df):

    attain = edu_df[1:25].copy()

    less_than_12th = [
        "Nursery school",
        "Kindergarten",
        "1st grade",
        "2nd grade",
        "3rd grade",
        "4th grade",
        "5th grade",
        "6th grade",
        "7th grade",
        "8th grade",
        "9th grade",
        "10th grade",
        "11th grade"
    ]

    less_than_12th_total = attain.loc[
        attain["groups"].isin(less_than_12th),
        "values"
    ].sum()

    attain = attain[
        ~attain["groups"].isin(less_than_12th)
    ].copy()

    less_than_row = pd.DataFrame({
        "groups": ["Less than 12th grade"],
        "values": [less_than_12th_total]
    })

    attain = pd.concat(
        [attain, less_than_row],
        ignore_index=True
    )

    order = [
        "No schooling completed",
        "Less than 12th grade",
        "12th grade, no diploma",
        "Regular high school diploma",
        "GED or alternative credential",
        "Some college, less than 1 year",
        "Some college, 1 or more years, no degree",
        "Associate's degree",
        "Bachelor's degree",
        "Master's degree",
        "Professional school degree",
        "Doctorate degree"
    ]

    attain["groups"] = pd.Categorical(
        attain["groups"],
        categories=order,
        ordered=True
    )

    attain = attain.sort_values("groups").reset_index(drop=True)

    return attain

def edu_enrollment_processing(edu_df):
    enroll = edu_df.iloc[64:71].copy()
    
    enroll['groups'] = enroll['groups'].str.replace("Enrolled: ", "", regex=False)
    
    return enroll

def edu_tech_access_processing(edu_df):
  tech = edu_df.iloc[122:127].copy()
  return tech

def edu_internet_processing(edu_df):
  internet = edu_df.iloc[128:].copy()

  #Shorten the text on broadband
  internet.at[131, 'groups'] = 'Broadband (cable, fiber optic, or DSL)'
  return internet


#🟩🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦ECONOMIC PROCESSING🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟩
# Labor force (population over 16 labor force)
def employ_labor_processing(employ_df):
  labor = employ_df.iloc[3:7].copy()
  return labor

# Work Commuters (population over 16 commuting excluding WFH row)
def employ_commute_processing(employ_df):
    commute = employ_df.iloc[89:103].copy()

    # Rename rows
    commute.at[89, 'groups'] = 'Car, truck, or van (alone)'
    commute.at[90, 'groups'] = 'Car, truck, or van (carpool)'

    # Drop summary rows
    commute = commute.drop(index=[91, 97])

    # Remove rows where values == 0
    commute = commute[commute["values"] != 0]

    return commute

# Commute Length 
def employ_commute_length_processing(employ_df):
  commute_length = employ_df.iloc[104:116].copy()

  return commute_length

#Earnings Gendered, Earnings by Ed Attainment
#Just present as numbers, not viz
def employ_gender_earnings_processing(employ_df):
  gender_earnings = employ_df[117:121].copy()
  return gender_earnings

# Earnings by Eduction (Just numbers, no viz)
def employ_ed_earnings_processing(employ_df):
  ed_earnings = employ_df[122:].copy()
  return ed_earnings