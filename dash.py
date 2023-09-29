import streamlit as st
import pandas as pd

# Exibir o logotipo centralizado com tamanho 200x200
st.image("farma.png", use_column_width=False, caption="", output_format="PNG", width=200)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])  # Lê todas as colunas

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "Complemento", "% Ressarcimento", "Status"]

# Função para formatar o valor em "R$ 75.809.091,57"
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(".", ",")

# Widget de seleção de status
status_selecionado = st.selectbox("Selecione o Status:", df["Status"].unique())

# Filtrar dados pelo status selecionado
dados_status_selecionado = df[df["Status"] == status_selecionado]

# Filtro de Lojas
lojas = dados_status_selecionado["Loja"].unique()
lojas_selecionadas = st.multiselect("Selecione as lojas:", lojas, default=lojas, key="lojas", help="Escolha uma ou mais lojas")

# Filtrar dados das lojas selecionadas
dados_lojas_selecionadas = dados_status_selecionado[dados_status_selecionado["Loja"].isin(lojas_selecionadas)]

# Organizar os blocos de total em uma grade
total_container = st.container()
total_block = st.columns(5)

# Estilo para centralizar e formatar os valores
value_style = "display: flex; justify-content: center; align-items: center; text-align: center; border: 2px solid #FF6400; padding: 10px; font-size: 20px;"

# Bloco de Faturamento ST
with total_block[0]:
    st.subheader("Faturamento ST")
    total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_faturamento_st)}</div>', unsafe_allow_html=True)

# Bloco de Ressarcimento
with total_block[1]:
    st.subheader("Ressarcimento")
    total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_ressarcimento)}</div>', unsafe_allow_html=True)

# Bloco de Complemento
with total_block[2]:
    st.subheader("Complemento")
    total_complemento = dados_lojas_selecionadas["Complemento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_complemento)}</div>', unsafe_allow_html=True)

# Bloco de Diferença Ressarcimento - Complemento
with total_block[3]:
    st.subheader("Ressarcimento - Compl")
    diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
    st.markdown(f'<div style="{value_style}">{formatar_valor(diferenca_ressarcimento_complemento)}</div>', unsafe_allow_html=True)

# Bloco de Média % Ressarcimento
with total_block[4]:
    st.subheader("Média % Ressarcimento")

    if status_selecionado == "Não Iniciado":
        st.write("Apenas nos outros Status")
    else:
        # Certifique-se de que a variável dados_lojas_selecionadas foi definida
        if "dados_lojas_selecionadas" in locals():
            media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean() * 100
        else:
            media_percentual_ressarcimento = 0.0

        st.markdown(f'<div style="{value_style}">{media_percentual_ressarcimento:.1f}%</div>', unsafe_allow_html=True)

        # Widget de entrada para a porcentagem
        nova_porcentagem = st.number_input("Nova Porcentagem (%)", min_value=0.0, max_value=100.0, value=media_percentual_ressarcimento / 100)

# Calcular o novo valor de ressarcimento com base na nova porcentagem
if status_selecionado != "Não Iniciado":
    novo_ressarcimento = total_faturamento_st * nova_porcentagem
    st.markdown(f'<div style="{value_style}">Novo Ressarcimento: {formatar_valor(novo_ressarcimento)}</div>', unsafe_allow_html=True)




# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Faturamento ST"], use_container_width=True)

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"], use_container_width=True)

# Gráfico de Barras (Complemento)
st.subheader("Gráfico de Barras (Complemento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Complemento"], use_container_width=True)
