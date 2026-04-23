from utils.processing import clean_race_data_single, clean_housing_data, clean_age_sex_data, clean_education_18_24, clean_ed_earnings_25_plus
import plotly as px
import pandas as pd
#Not the best way to import this, but i want to keep plotly
import plotly.express as pxx
import plotly.graph_objects as go
import streamlit as st
from utils.data_loader import read_csv_fallback

df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')
df4 = read_csv_fallback('data/Lawrence GWI Education.csv')

#save cleaned datasets as variables
cleaned_race_single = clean_race_data_single(df1)
cleaned_housing = clean_housing_data(df2)
cleaned_age_gender = clean_age_sex_data(df3)
cleaned_ed_18_24 = clean_education_18_24(df4)
cleaned_ed_earnings_25_plus = clean_ed_earnings_25_plus(df4)


'''
RACE BY AGE VISUALIZATION

Start with male and female 
    data = clean_female and cleaned_male
    merge and add values on the Age Group column
    Create a gold medal by country similar visualization, stacked bar chart by age category

    What does the data look like in this df do this in colab

    
https://plotly.com/python/bar-charts/

            nation   medal  count
0  South Korea    gold     24
1        China    gold     10
2       Canada    gold      9
3  South Korea  silver     13
4        China  silver     15
5       Canada  silver     12
6  South Korea  bronze     11
7        China  bronze      8
8       Canada  bronze     12


Ideal format
            gender Age Group   amount
0           Male    AG1     male count AG1
1          Female   AG1     Female count AG1
2           Male    AG2     male count AG2
3          Female   AG2     Female count AG2
4           Male    AG3     male count AG3
5          Female   AG3     Female count AG3

                to the end

# Visualization for Age Gender Distribution


'''
# Visualization for Age Gender Distribution


def plot_age_gender(age_sex):
    #reorder our new categories
    order = [
    "Under 5", "5–9", "10–17", "18–24",
    "25–34", "35–44", "45–54",
    "55–64", "65–74", "75–84", "85+"
]

    age_sex["Age Group"] = pd.Categorical(age_sex["Age Group"], categories=order, ordered=True)
    age_sex = age_sex.sort_values("Age Group")

    
    fig = pxx.bar(
        age_sex,
        x="Age Group",
        y="Estimate",
        color="Gender",
        text="Gender"
    )

    fig.update_layout(
        title={
            "text": "Population Distribution by Age Group and Gender in Lawrence, MA",
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="Age Group",
        yaxis_title="Population"
    )

    fig.update_layout(xaxis_tickangle=-45)

    return fig

def plot_housing(housing_data):
    # Visualization
    labels = housing_data['Categories']
    values = housing_data['Estimate']

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    return fig


'''
Function for plotting cleaned Employment data
Function for plotting cleaned Education data
'''

def plot_education_18_24(ed_data):
    labels = ed_data['Groups']
    values = ed_data['Estimate']
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        title={
            "text": "Distribution of Education Attainment for 18-24 Year Olds in Lawrence, MA",
            "x": 0.44,
            "xanchor": "center"
        })
    return fig


def plot_education_25_plus(ed_data):
    fig = pxx.bar(ed_data, x='Groups', y='Estimate', hover_data=['Groups', 'Estimate', 'Margin of Error'], color='Estimated Salary', labels={'Groups': 'Education Attainment Groups'}, height=400)
    fig.update_layout(
        title={
            "text": "Title",
            "x": 0.44,
            "xanchor": "center"
        })
    return fig


#This will need to be changed for other cities, or maybe not we can just address it like how
#we will here
def plot_race(race_data):
    race_data = race_data.copy()

    race_data['Resident Count'] = (
    race_data['Resident Count']
    .astype(str)
    .str.replace(',', '', regex=True)
    .str.strip()
)
    race_data['Resident Count'] = pd.to_numeric(race_data['Resident Count'], errors='coerce')

    plot_race_data = race_data[race_data['Resident Count'] > 0]
    fig = pxx.bar(plot_race_data, x='Race', y='Resident Count')
    fig.update_layout(
        title={
            "text": "Race Distribution in Lawrence<br><sup>Note: Unreported Categories: American Indian and Alaska Native alone and Native Hawaiian and Other Pacific Islander alone</sup>",
            "x": 0.5,
            "xanchor": "center"
        }
    )
    return fig
