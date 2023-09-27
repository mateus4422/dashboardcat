import streamlit as st
import pandas as pd

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8], skiprows=1)

# Renomear as colunas
df.columns = ["Periodo Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Filtro de Lojas
lojas = df["Loja"].unique()
loja_selecionada = st.selectbox("Selecione uma loja:", ["Geral"] + list(lojas))

# Filtrar dados da loja selecionada
if loja_selecionada == "Geral":
    dados_loja = df  # Exibir todos os dados
else:
    dados_loja = df[df["Loja"] == loja_selecionada]  # Filtrar dados da loja selecionada

# Resumo Geral
st.write("Resumo Geral:")

# Bloco de Total Faturamento ST
st.subheader("Total Faturamento ST (Milhões de Reais)")
total_faturamento_st = dados_loja["Faturamento ST"].sum() / 1_000_000
st.write(f"{total_faturamento_st:.2f} Milhões de Reais")

# Bloco de Total Ressarcimento
st.subheader("Total Ressarcimento (Milhões de Reais)")
total_ressarcimento = dados_loja["Ressarcimento"].sum() / 1_000_000
st.write(f"{total_ressarcimento:.2f} Milhões de Reais")

# Bloco de Média % Ressarcimento
st.subheader("Média % Ressarcimento")
media_percentual_ressarcimento = dados_loja["% Ressarcimento"].mean() * 100
st.write(f"{media_percentual_ressarcimento:.2f}%")
