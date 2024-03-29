import streamlit as st
from analise_pede import load_pede_data
from analise_pse2020 import load_pse2020

def dados_brutos():
    st.write("PEDE")
    df_pede = load_pede_data()
    st.write(df_pede.head())

    st.write("PSE")
    df_pse = load_pse2020()
    st.write(df_pse.head())