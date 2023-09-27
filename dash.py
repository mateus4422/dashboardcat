import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega os dados do Excel online
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=csv"
df = pd.read_csv(url)

# Título do dashboard
st.title("Dashboard de Análise de Lojas")

# Filtro de Loja
loja_filtrada = st.selectbox("Selecione a Loja:", df["Loja"].unique())

# Filtro de Período Inicial
periodo_inicial_filtrado = st.selectbox("Selecione o Período Inicial:", df["Período Inicial"].unique())

# Filtra os dados com base na loja e no período inicial selecionados
df_filtrado = df[(df["Loja"] == loja_filtrada) & (df["Período Inicial"] == periodo_inicial_filtrado)]

# Exibe os dados da loja selecionada
st.write("Dados da Loja:", loja_filtrada)
st.write(df_filtrado)

# Gráfico de Faturamento ST e Ressarcimento usando Plotly
fig1 = px.bar(df_filtrado, x="Ano Mês", y=["Faturamento ST", "Ressarcimento"], title="Faturamento ST vs. Ressarcimento")
st.plotly_chart(fig1)

# Gráfico de % Ressarcimento usando Plotly
fig2 = px.line(df_filtrado, x="Ano Mês", y="% Ressarcimento", title="% Ressarcimento ao longo do tempo")
st.plotly_chart(fig2)
