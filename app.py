import streamlit as st
from utils.data_loader import read_csv_fallback
from utils.processing import clean_race_data_single, clean_race_data_mixed, clean_housing_data, clean_age_sex_data
from utils.visualization import plot_age_gender, plot_housing


st.title('Lawrence GWI')

try:
	df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
	df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
	df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')
except Exception as e:
	st.error(f"Failed to load CSV files: {e}")
	st.stop()

#save cleaned datasets as variables
cleaned_race_single = clean_race_data_single(df1)
cleaned_race_mixed = clean_race_data_mixed(df1)
cleaned_housing = clean_housing_data(df2)
cleaned_age_gender = clean_age_sex_data(df3)

tab1, tab2, tab3, tab4= st.tabs(["Home", "Demographics", "Housing", "Gender Distribution"])

with tab1:
    st.header("Welcome to the Lawrence GWI Dashboard")
with tab2:
    st.header("Demographics")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    st.write("Preview of Data 1")
    st.dataframe(cleaned_race_single)
    st.dataframe(cleaned_race_mixed)

with tab3:
    st.header("Housing Information")
    st.write('Preview of Data 2')
    fig = plot_housing(cleaned_housing)
    st.plotly_chart(fig)
    st.dataframe(cleaned_housing)
with tab4:
    st.header("Gender Distribution by Age")
    fig = plot_age_gender(cleaned_age_gender)
    st.plotly_chart(fig)
    st.write('Preview of Data 3')
    st.dataframe(cleaned_age_gender)
