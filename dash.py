import streamlit as st
import pandas as pd

# Exibir o logotipo
st.image("farma.png", use_column_width=False, width=300)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8], skiprows=1)

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Filtro de Lojas
lojas = df["Loja"].unique()
lojas_selecionadas = st.multiselect("Selecione as lojas:", lojas, default=["Geral"])

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

# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Faturamento ST"])

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"])
