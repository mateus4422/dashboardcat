import streamlit as st
import pandas as pd

# Carregar os dados do Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pubhtml"
df = pd.read_html(url)[0]

# Filtrar os dados para P1 e P2 com base nas datas
df["Período Inicial"] = pd.to_datetime(df["Período Inicial"], dayfirst=True)
df["Período Final"] = pd.to_datetime(df["Período Final"], dayfirst=True)
p1_mask = (df["Período Inicial"] >= "2018-05-01") & (df["Período Final"] <= "2019-09-30")
p2_mask = (df["Período Inicial"] >= "2019-09-01") & (df["Período Final"] <= "2020-10-31")

# Adicionar coluna "Período" com valores P1 e P2
df["Período"] = ""
df.loc[p1_mask, "Período"] = "P1"
df.loc[p2_mask, "Período"] = "P2"

# Filtros
st.sidebar.title("Filtros")
lojas = st.sidebar.multiselect("Lojas", df["Loja"].unique())
geral = st.sidebar.checkbox("Geral")

# Filtrar dados com base nos filtros selecionados
if geral:
    filtered_df = df
else:
    filtered_df = df[df["Loja"].isin(lojas)]

# Mostrar dados
st.title("Dados das Lojas")
st.write(filtered_df)

if geral:
    st.title("Dados Gerais")
    st.write("Faturamento ST Total:", filtered_df["Faturamento ST"].sum())
    st.write("Ressarcimento Total:", filtered_df["Ressarcimento"].sum())
    st.write("% Ressarcimento Total:", filtered_df["% Ressarcimento"].mean())
