import streamlit as st
import pandas as pd

# Exibir o logotipo
st.image("farma.png", use_column_width=False, width=300)

# Definir o CSS personalizado
st.markdown(
    """
    <style>
        .st-ff6400 {
            background-color: #FF6400;
        }
        .st-ff6400:hover {
            background-color: #FF6400;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])  # Lê todas as colunas

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "Complemento", "% Ressarcimento", "Status"]

# Filtro de Lojas
lojas = df["Loja"].unique()
lojas_selecionadas = st.multiselect("Selecione as lojas:", lojas, default=lojas, key="lojas", help="Escolha uma ou mais lojas")

# Filtrar dados das lojas selecionadas
dados_lojas_selecionadas = df[df["Loja"].isin(lojas_selecionadas)]

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

# Bloco de Total Complemento
st.subheader("Total Complemento")
total_complemento = dados_lojas_selecionadas["Complemento"].sum()
st.write(f"R$ {total_complemento:,.2f}")

# Bloco de Ressarcimento - Complemento
st.subheader("Ressarcimento - Complemento")
diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
st.write(f"R$ {diferenca_ressarcimento_complemento:,.2f}")

# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Faturamento ST"], use_container_width=True)

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"], use_container_width=True)

# Gráfico de Barras (Complemento)
st.subheader("Gráfico de Barras (Complemento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Complemento"], use_container_width=True)

# Gráfico de Barras (Ressarcimento - Complemento)
st.subheader("Gráfico de Barras (Ressarcimento - Complemento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"] - dados_lojas_selecionadas.set_index("Loja")["Complemento"], use_container_width=True)
