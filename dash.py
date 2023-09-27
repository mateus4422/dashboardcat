import streamlit as st
import pandas as pd

# Carregar os dados do Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pubhtml"
df = pd.read_html(url)[0]

# Mostrar as colunas disponíveis
st.write("Colunas Disponíveis:")
st.write(df.columns)

# Sidebar com filtro de lojas
st.sidebar.header("Filtro de Lojas")
lojas = df["Loja"].unique()
selected_lojas = st.sidebar.multiselect("Selecione as Lojas:", lojas)

# Filtro de dados com base nas lojas selecionadas
filtered_df = df[df["Loja"].isin(selected_lojas)]

# Mostrar os dados filtrados
st.write("Dados das Lojas Selecionadas:")
st.write(filtered_df)

# Resumo Geral
st.header("Resumo Geral")
st.write("Total de Faturamento ST:", filtered_df["Faturamento ST"].sum())
st.write("Total de Ressarcimento:", filtered_df["Ressarcimento"].sum())
st.write("% Ressarcimento Médio:", filtered_df["% Ressarcimento"].mean())
st.write("Status Mais Comum:", filtered_df["Status"].mode().values[0])
