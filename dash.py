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

# Checkbox para Lojas com Prioridade
mostrar_lojas_com_prioridade = st.checkbox("Lojas com Prioridade")

# Filtrar dados pelo status selecionado
dados_status_selecionado = df[df["Status"] == status_selecionado]

# Filtrar dados por lojas com prioridade, se a opção estiver marcada
if mostrar_lojas_com_prioridade:
    dados_status_selecionado = dados_status_selecionado[dados_status_selecionado["Prioridade"] == "Sim"]

# Organizar os blocos de total em uma grade
total_container = st.container()
total_block = st.columns(5)

# Estilo para centralizar e formatar os valores
value_style = "display: flex; justify-content: center; align-items: center; text-align: center; border: 2px solid #FF6400; padding: 10px; font-size: 20px;"

# Bloco de Faturamento ST
with total_block[0]:
    st.subheader("Faturamento ST")
    total_faturamento_st = dados_status_selecionado["Faturamento ST"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_faturamento_st)}</div>', unsafe_allow_html=True)

# Bloco de Ressarcimento
with total_block[1]:
    st.subheader("Ressarcimento")
    total_ressarcimento = dados_status_selecionado["Ressarcimento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_ressarcimento)}</div>', unsafe_allow_html=True)

# Bloco de Complemento
with total_block[2]:
    st.subheader("Complemento")
    total_complemento = dados_status_selecionado["Complemento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_complemento)}</div>', unsafe_allow_html=True)

# Bloco de Diferença Ressarcimento - Complemento
with total_block[3]:
    st.subheader("Ressarcimento - Compl")
    diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
    st.markdown(f'<div style="{value_style}">{formatar_valor(diferenca_ressarcimento_complemento)}</div>', unsafe_allow_html=True)

# Calculadora de Média % Ressarcimento apenas para "Em Desenvolvimento"
if status_selecionado == "Em Desenvolvimento":
    with total_block[4]:
        st.subheader("Média % Ressarcimento")
        
        if not dados_status_selecionado.empty:
            media_percentual_ressarcimento = dados_status_selecionado["% Ressarcimento"].mean() * 100
            st.markdown(f'<div style="{value_style}">{media_percentual_ressarcimento:.1f}%</div>', unsafe_allow_html=True)

            # Widget de entrada para a porcentagem
            nova_porcentagem = st.number_input("Nova Porcentagem (%)", min_value=0.0, max_value=100.0, value=media_percentual_ressarcimento)
            
            # Calcular o novo valor de ressarcimento com base na nova porcentagem
            novo_ressarcimento = total_faturamento_st * (nova_porcentagem / 100)
            st.markdown(f'<div style="{value_style}">Novo Ressarcimento: {formatar_valor(novo_ressarcimento)}</div>', unsafe_allow_html=True)
        else:
            st.write("Apenas nos Status 'Em Desenvolvimento'")
else:
    with total_block[4]:
        st.subheader("Média % Ressarcimento")
        st.write("Apenas nos outros Status")

# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_status_selecionado.set_index("Loja")["Faturamento ST"], use_container_width=True)

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_status_selecionado.set_index("Loja")["Ressarcimento"], use_container_width=True)

# Gráfico de Barras (Complemento)
st.subheader("Gráfico de Barras (Complemento)")
st.bar_chart(dados_status_selecionado.set_index("Loja")["Complemento"], use_container_width=True)
