import streamlit as st
import pandas as pd

# Definir o CSS personalizado para centralizar a imagem
st.markdown(
    """
    <style>
        .centered-image {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exibir o logotipo centralizado com tamanho 200x200
st.markdown('<div class="centered-image"><img src="farma.png" width="200" height="200"></div>', unsafe_allow_html=True)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8])

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
st.markdown('<div class="centered-image"><p>Total Faturamento ST</p></div>', unsafe_allow_html=True)
total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
st.markdown(f'<div class="centered-image"><p style="font-size:24px;">R$ {total_faturamento_st:,.2f}</p></div>', unsafe_allow_html=True)

# Bloco de Total Ressarcimento
st.markdown('<div class="centered-image"><p>Total Ressarcimento</p></div>', unsafe_allow_html=True)
total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
st.markdown(f'<div class="centered-image"><p style="font-size:24px;">R$ {total_ressarcimento:,.2f}</p></div>', unsafe_allow_html=True)

# Bloco de Total Complemento
st.markdown('<div class="centered-image"><p>Total Complemento</p></div>', unsafe_allow_html=True)
total_complemento = dados_lojas_selecionadas["Complemento"].sum()
st.markdown(f'<div class="centered-image"><p style="font-size:24px;">R$ {total_complemento:,.2f}</p></div>', unsafe_allow_html=True)

# Bloco de Ressarcimento - Complemento
st.markdown('<div class="centered-image"><p>Ressarcimento - Complemento</p></div>', unsafe_allow_html=True)
ressarcimento_minus_complemento = total_ressarcimento - total_complemento
st.markdown(f'<div class="centered-image"><p style="font-size:24px;">R$ {ressarcimento_minus_complemento:,.2f}</p></div>', unsafe_allow_html=True)

# Média % Ressarcimento
st.subheader("Média % Ressarcimento")
media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean()
st.write(f"{media_percentual_ressarcimento:.2%}")

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
