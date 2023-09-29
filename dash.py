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
lojas = df["Loja"].unique()
# Inicialmente, não há necessidade de definir um valor padrão para o multiselect
lojas_selecionadas = st.multiselect("Selecione as lojas:", lojas, key="lojas", help="Escolha uma ou mais lojas")

# Filtrar dados por status
status = df["Status"].unique()
selected_status = st.radio("Selecione o Status:", status)

# Filtrar os dados com base no status selecionado
filtered_data = df[df["Status"] == selected_status]

# Verificar se há dados para o status selecionado
if filtered_data.empty:
    st.warning(f"Nenhum dado encontrado para o status '{selected_status}'.")
else:
    # Organizar os blocos de total em uma grade
    total_container = st.container()
    total_block = st.columns(5)

    # Estilo para centralizar e formatar os valores
    value_style = "display: flex; justify-content: center; align-items: center; text-align: center; border: 2px solid #FF6400; padding: 10px; font-size: 20px;"

    # Função para formatar o valor em "R$ 75.809.091,57"
    def formatar_valor(valor):
        return f"R$ {valor:,.2f}".replace(".", ",")

    # Bloco de Faturamento ST
    with total_block[0]:
        st.subheader("Faturamento ST")
        total_faturamento_st = filtered_data["Faturamento ST"].sum()
        st.markdown(f'<div style="{value_style}">{formatar_valor(total_faturamento_st)}</div>', unsafe_allow_html=True)

    # Bloco de Ressarcimento
    with total_block[1]:
        st.subheader("Ressarcimento")
        total_ressarcimento = filtered_data["Ressarcimento"].sum()
        st.markdown(f'<div style="{value_style}">{formatar_valor(total_ressarcimento)}</div>', unsafe_allow_html=True)

    # Bloco de Complemento
    with total_block[2]:
        st.subheader("Complemento")
        total_complemento = filtered_data["Complemento"].sum()
        st.markdown(f'<div style="{value_style}">{formatar_valor(total_complemento)}</div>', unsafe_allow_html=True)

    # Bloco de Diferença Ressarcimento - Complemento
    with total_block[3]:
        st.subheader("Ressarcimento - Compl")
        diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
        st.markdown(f'<div style="{value_style}">{formatar_valor(diferenca_ressarcimento_complemento)}</div>', unsafe_allow_html=True)

    # Média % Ressarcimento geral (multiplicada por 100)
    media_percentual_ressarcimento = filtered_data["% Ressarcimento"].mean() * 100

    # Bloco de Média % Ressarcimento
    with total_block[4]:
        st.subheader("Média % Ressarcimento")
        st.markdown(f'<div style="{value_style}">{media_percentual_ressarcimento:.1f}%</div>', unsafe_allow_html=True)

    # Gráfico de Barras (Faturamento ST)
    st.subheader("Gráfico de Barras (Faturamento ST)")
    st.bar_chart(filtered_data.set_index("Loja")["Faturamento ST"], use_container_width=True)

    # Gráfico de Barras (Ressarcimento)
    st.subheader("Gráfico de Barras (Ressarcimento)")
    st.bar_chart(filtered_data.set_index("Loja")["Ressarcimento"], use_container_width=True)

    # Gráfico de Barras (Complemento)
    st.subheader("Gráfico de Barras (Complemento)")
    st.bar_chart(filtered_data.set_index("Loja")["Complemento"], use_container_width=True)
