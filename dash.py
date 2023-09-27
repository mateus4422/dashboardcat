import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8], skiprows=0)  # Agora começa da primeira linha (skiprows=0)

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Adicionar coluna de P1 ou P2 com base nas datas
df["P1_P2"] = "P1"  # Inicialmente, todas as linhas são definidas como P1
df.loc[df["Período Inicial"] >= "2019-09-01", "P1_P2"] = "P2"  # Definir como P2 se a data inicial for posterior a 01/09/2019

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
st.subheader("Total Faturamento ST")
total_faturamento_st = dados_loja["Faturamento ST"].sum()
st.write(f"R$ {total_faturamento_st:,.2f}")

# Bloco de Total Ressarcimento
st.subheader("Total Ressarcimento")
total_ressarcimento = dados_loja["Ressarcimento"].sum()
st.write(f"R$ {total_ressarcimento:,.2f}")

# Bloco de Média % Ressarcimento
st.subheader("Média % Ressarcimento")
media_percentual_ressarcimento = dados_loja["% Ressarcimento"].mean()
st.write(f"{media_percentual_ressarcimento:.2%}")

# Gráfico comparando faturamento e ressarcimento para P1 e P2
fig = px.scatter(
    dados_loja, x="Faturamento ST", y="Ressarcimento", color="P1_P2",
    labels={"Faturamento ST": "Faturamento ST (R$)", "Ressarcimento": "Ressarcimento (R$)"},
    title="Comparação de Faturamento e Ressarcimento (P1 vs. P2)"
)
st.plotly_chart(fig)
