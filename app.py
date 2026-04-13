import streamlit as st
from utils.data_loader import read_csv_fallback


st.title('Lawrence GWI')

try:
	df1 = read_csv_fallback('data/Lawrence GWI Race.csv')
	df2 = read_csv_fallback('data/Lawrence GWI Renter.csv')
	df3 = read_csv_fallback('data/Lawrence GWI Sex by Age.csv')
except Exception as e:
	st.error(f"Failed to load CSV files: {e}")
	st.stop()

#st.write("Preview of Data 1")
#st.dataframe(df1.head())

tab1, tab2, tab3, tab4= st.tabs(["Home", "Df1", "Df2", "Df3"])

with tab1:
    st.header("Welcome to the Lawrence GWI Dashboard")
with tab2:
    st.header("Demographics")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    st.write("Preview of Data 1")
    st.dataframe(df1.iloc[1:9])
with tab3:
    st.header("Housing Information")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    st.write('Preview of Data 2')
    st.dataframe(df2.head())
with tab4:
    st.header("Gender Distribution by Age")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    st.write('Preview of Data 3')
    st.dataframe(df3)
