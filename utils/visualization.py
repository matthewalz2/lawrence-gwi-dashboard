from utils.processing import clean_race_data_single, clean_race_data_mixed, clean_housing_data, clean_age_sex_data_f, clean_age_sex_data_m
import plotly as px
import streamlit as st
from utils.data_loader import read_csv_fallback

df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')

#save cleaned datasets as variables
cleaned_race_single = clean_race_data_single(df1)
cleaned_race_mixed = clean_race_data_mixed(df1)
cleaned_housing = clean_housing_data(df2)
cleaned_female = clean_age_sex_data_f(df3)
cleaned_male = clean_age_sex_data_m(df3)

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



'''







