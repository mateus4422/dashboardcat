import streamlit as st
import pandas as pd

# Exibir o logotipo centralizado com tamanho 200x200
st.image("farma.png", use_column_width=False, caption="Logo", output_format="PNG", width=200)

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
total_block = st.columns(5)

# Estilo para centralizar e formatar os valores
value_style = "display: flex; justify-content: center; align-items: center; text-align: center; border: 2px solid #FF6400; padding: 10px; font-size: 20px;"

# Função para inverter vírgulas e pontos
def inverter_pontuacao(text):
    return text.replace(",", "|").replace(".", ",").replace("|", ".")

# Bloco de Faturamento ST
with total_block[0]:
    st.subheader("Faturamento ST")
    total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
    total_faturamento_st_formatted = inverter_pontuacao(f"R$ {total_faturamento_st:.2f}")
    st.markdown(f'<div style="{value_style}">{total_faturamento_st_formatted}</div>', unsafe_allow_html=True)

# Bloco de Ressarcimento
with total_block[1]:
    st.subheader("Ressarcimento")
    total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
    total_ressarcimento_formatted = inverter_pontuacao(f"R$ {total_ressarcimento:.2f}")
    st.markdown(f'<div style="{value_style}">{total_ressarcimento_formatted}</div>', unsafe_allow_html=True)

# Bloco de Complemento
with total_block[2]:
    st.subheader("Complemento")
    total_complemento = dados_lojas_selecionadas["Complemento"].sum()
    total_complemento_formatted = inverter_pontuacao(f"R$ {total_complemento:.2f}")
    st.markdown(f'<div style="{value_style}">{total_complemento_formatted}</div>', unsafe_allow_html=True)

# Bloco de Diferença Ressarcimento - Complemento
with total_block[3]:
    st.subheader("Diferença Ressarcimento - Complemento")
    diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
    diferenca_ressarcimento_complemento_formatted = inverter_pontuacao(f"R$ {diferenca_ressarcimento_complemento:.2f}")
    st.markdown(f'<div style="{value_style}">{diferenca_ressarcimento_complemento_formatted}</div>', unsafe_allow_html=True)

# Bloco de Média % Ressarcimento
with total_block[4]:
    st.subheader("Média % Ressarcimento")
    media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean()
    media_percentual_ressarcimento_formatted = inverter_pontuacao(f"{media_percentual_ressarcimento:.2%}")
    st.markdown(f'<div style="{value_style}">{media_percentual_ressarcimento_formatted}</div>', unsafe_allow_html=True)

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

# Gráfico de Barras (Diferença Ressarcimento - Complemento)
st.subheader("Gráfico de Barras (Diferença Ressarcimento - Complemento)")
st.bar_chart([diferenca_ressarcimento_complemento], use_container_width=True)
