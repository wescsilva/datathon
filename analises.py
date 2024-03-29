import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from io import BytesIO
import plotly.express as px

from analise_pede import analise_pede
from analise_pse2020 import analise_pse2020
from dados_brutos import dados_brutos

def realizar_analise():
    aba1, aba2, aba3 = st.tabs(['Análise PEDE', 'Análise PSE2020', 'Dados Brutos'])    
    
    with aba1:
        analise_pede()
    
    with aba2:
        analise_pse2020()
    
    with aba3:
        dados_brutos()

        
        
