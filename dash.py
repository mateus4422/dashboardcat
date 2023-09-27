import streamlit as st
import pandas as pd

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[2, 3, 4, 5, 6, 7, 8, 9], skiprows=1)

# Renomear as colunas
df.columns = ["Periodo Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Exibir os dados
st.write(df)
