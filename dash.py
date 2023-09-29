import streamlit as st
import pandas as pd
import plotly.express as px

# Exibir o logotipo centralizado com tamanho 200x200
st.image("farma.png", use_column_width=False, caption="", output_format="PNG", width=200)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])  # Lê todas as colunas

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "Complemento", "% Ressarcimento", "Status"]

# Filtro de Lojas
lojas = ["Selecionar Todos"] + df["Loja"].unique().tolist()
lojas_selecionadas = st.multiselect("Selecione as lojas:", lojas, default=lojas, key="lojas", help="Escolha uma ou mais lojas")

# Filtrar dados das lojas selecionadas
if "Selecionar Todos" not in lojas_selecionadas:
    dados_lojas_selecionadas = df[df["Loja"].isin(lojas_selecionadas)]
else:
    dados_lojas_selecionadas = df  # Mostrar todos os dados

# Verifica se o status é diferente de "Não Iniciado" para exibir a calculadora
if "Não Iniciado" not in lojas_selecionadas:
    # Média % Ressarcimento geral (multiplicada por 100)
    media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean() * 100

    # Bloco de Média % Ressarcimento
    st.subheader("Média % Ressarcimento")
    nova_porcentagem = st.number_input("Nova Porcentagem (%)", min_value=0.0, max_value=100.0, value=media_percentual_ressarcimento / 100)
    novo_ressarcimento = nova_porcentagem * dados_lojas_selecionadas["Faturamento ST"].sum() / 100
    st.markdown(f'<div style="{value_style}">{formatar_valor(novo_ressarcimento)}</div>', unsafe_allow_html=True)

# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Faturamento ST"], use_container_width=True)

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"], use_container_width=True)

# Gráfico de Barras (Complemento)
st.subheader("Gráfico de Barras (Complemento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Complemento"], use_container_width=True)
