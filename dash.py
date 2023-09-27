import streamlit as st
import pandas as pd

# Link para o arquivo do Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pubhtml"

# Lê os dados do Google Sheets
df = pd.read_html(url)[0]

# Filtra os dados por Loja
lojas = df["Loja"].unique()
filtro_loja = st.selectbox("Selecione uma Loja:", lojas)
df_loja = df[df["Loja"] == filtro_loja]

# Exibe os dados da Loja selecionada
st.write(f"**Loja:** {filtro_loja}")
st.write(f"**CNPJ:** {df_loja['CNPJ'].iloc[0]}")
st.write(f"**Faturamento ST:** {df_loja['Faturamento ST'].iloc[0]}")
st.write(f"**Ressarcimento:** {df_loja['Ressarcimento'].iloc[0]}")
st.write(f"**% Ressarcimento:** {df_loja['% Ressarcimento'].iloc[0]}")
st.write(f"**Status:** {df_loja['Status'].iloc[0]}")
