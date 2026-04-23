import streamlit as st
from utils.data_loader import read_csv_fallback
from utils.processing import clean_ed_earnings_25_plus, clean_race_data_single, clean_housing_data, clean_age_sex_data, clean_education_18_24
from utils.visualization import plot_age_gender, plot_housing, plot_education_18_24, plot_education_25_plus, plot_race


st.title('Lawrence GWI')

try:
    df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
    df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
    df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')
    df4 = read_csv_fallback('data/Lawrence GWI Education.csv')
except Exception as e:
    st.error(f"Failed to load CSV files: {e}")
    st.stop()

#save cleaned datasets as variables
cleaned_race_single = clean_race_data_single(df1)
cleaned_housing = clean_housing_data(df2)
cleaned_age_gender = clean_age_sex_data(df3)
cleaned_ed_18_24 = clean_education_18_24(df4)
cleaned_ed_earnings_25_plus = clean_ed_earnings_25_plus(df4)

tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Home", "Demographics", "Housing", "Gender Distribution", "Education", "Economy"])


#Tab control for the main display
with tab1:
    st.header("Welcome to the Lawrence GWI Dashboard")
with tab2:
    st.header("Demographics")
    fig = plot_race(cleaned_race_single)
    st.plotly_chart(fig)
    st.write("Race Distribution in Lawrence")
    st.dataframe(cleaned_race_single)
    

with tab3:
    st.header("Housing Information")
    st.write('Property Renter and Owner Distribution')
    fig = plot_housing(cleaned_housing)
    st.plotly_chart(fig)
    st.dataframe(cleaned_housing)
with tab4:
    st.header("Gender Distribution by Age")
    fig = plot_age_gender(cleaned_age_gender)
    st.plotly_chart(fig)
    st.write('Preview of Data 3')
    st.dataframe(cleaned_age_gender)
with tab5:
    st.header("Education")
    fig = plot_education_18_24(cleaned_ed_18_24)
    fig2 = plot_education_25_plus(cleaned_ed_earnings_25_plus)
    st.plotly_chart(fig)
    st.write('Education Attainment of 18-24 Year Olds')
    st.dataframe(cleaned_ed_18_24)
    st.plotly_chart(fig2)
    st.write('Education Attainment of 25+ Year Olds')
    st.dataframe(cleaned_ed_earnings_25_plus)
with tab6:
    st.header("Economy")

