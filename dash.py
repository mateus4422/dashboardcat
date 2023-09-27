import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8], skiprows=0)  # Começa da primeira linha (skiprows=0)

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Adicionar coluna de P1 ou P2 com base nas datas
df["P1_P2"] = "P1"  # Inicialmente, todas as linhas são definidas como P1
df.loc[df["Período Inicial"] >= "2019-09-01", "P1_P2"] = "P2"  # Definir como P2 se a data inicial for posterior a 01/09/2019

# Calcular a média de ressarcimento da seguinte maneira: (Ressarcimeento - 100) / Faturamento
df["Media Ressarcimento"] = ((df["Ressarcimento"] - 100) / df["Faturamento ST"]) * 100

# Filtro de Lojas (checkboxes)
lojas = df["Loja"].unique()
lojas_selecionadas = st.multiselect("Selecione as lojas para comparação:", lojas, default=lojas)

# Filtrar dados das lojas selecionadas
if "Geral" in lojas_selecionadas:
    dados_lojas_selecionadas = df  # Exibir todos os dados
else:
    dados_lojas_selecionadas = df[df["Loja"].isin(lojas_selecionadas)]  # Filtrar dados das lojas selecionadas

# Resumo Geral
st.write("Resumo Geral:")

# Bloco de Total Faturamento ST
st.subheader("Total Faturamento ST")
total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
st.write(f"R$ {total_faturamento_st:,.2f}")

# Bloco de Total Ressarcimento
st.subheader("Total Ressarcimento")
total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
st.write(f"R$ {total_ressarcimento:,.2f}")

# Bloco de Média % Ressarcimento
st.subheader("Média % Ressarcimento")
media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean()
st.write(f"{media_percentual_ressarcimento:.2%}")

# Bloco de Média Ressarcimento (calculado)
st.subheader("Média Ressarcimento (calculado)")
media_ressarcimento_calculado = dados_lojas_selecionadas["Media Ressarcimento"].mean()
st.write(f"{media_ressarcimento_calculado:.2f}%")

# Gráfico de barras verticais para comparar Faturamento e Ressarcimento das Lojas selecionadas
fig = px.bar(dados_lojas_selecionadas, x="Loja", y=["Faturamento ST", "Ressarcimento"],
             labels={"Loja": "Loja", "value": "Valor (R$)"},
             title="Comparação de Faturamento e Ressarcimento das Lojas")
st.plotly_chart(fig)

# Exibir as lojas selecionadas
if "Geral" not in lojas_selecionadas:
    st.write("Lojas Selecionadas:")
    st.table(dados_lojas_selecionadas)
