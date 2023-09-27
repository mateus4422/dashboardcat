import streamlit as st
import pandas as pd

# Exibir o logotipo centralizado
st.image("farma.png", use_column_width=True, caption="", output_format="PNG", width=100)

# Adicionar linhas separadoras sublinhadas
st.markdown('<hr style="border:2px solid #FF6400">', unsafe_allow_html=True)

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

# Organizar os blocos de total em uma grade
total_container = st.container()
total_container.markdown('<hr style="border:2px solid #FF6400">', unsafe_allow_html=True)
total_block1, total_block2, total_block3, total_block4 = st.columns(4)

# Bloco de Total Faturamento ST
with total_block1:
    st.subheader("Total Faturamento ST")
    total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
    st.write(f"R$ {total_faturamento_st:,.2f}")

# Bloco de Total Ressarcimento
with total_block2:
    st.subheader("Total Ressarcimento")
    total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
    st.write(f"R$ {total_ressarcimento:,.2f}")

# Bloco de Total Complemento
with total_block3:
    st.subheader("Total Complemento")
    total_complemento = dados_lojas_selecionadas["Complemento"].sum()
    st.write(f"R$ {total_complemento:,.2f}")

# Bloco de Ressarcimento - Complemento
with total_block4:
    st.subheader("Ressarcimento - Complemento")
    diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
    st.write(f"R$ {diferenca_ressarcimento_complemento:,.2f}")

# Espaço em branco entre os blocos
st.markdown('<hr style="border:2px solid #FF6400">', unsafe_allow_html=True)

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
