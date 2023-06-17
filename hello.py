'''
Streamlit app homepage setup

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import streamlit as st
from PIL import Image

# Define a função para carregar informações sobre o app na sidebar
def load_about():
    st.sidebar.title("Sobre")
    st.sidebar.info(
        """
        Dúvidas ou sugestões, entre em contato:\n📩 vitorbeltrao300@gmail.com
        """
    )

# Configurações iniciais da página
st.set_page_config(
    page_title="Análise de Tweets do Atlético Mineiro",
    page_icon="⚽",
)

# Título e imagem do clube
st.title("Bem-vindo ao App de Análise de Tweets do Atlético Mineiro")
# image = Image.open("path/para/o/seu/logo.png")  # Substitua pelo caminho do seu logo
# st.image(image, use_column_width=True)

# Breve descrição do app
st.write("Este aplicativo permite analisar os dados dos tweets publicados pela página oficial do Clube Atlético Mineiro.")
st.write("Você pode explorar diferentes gráficos e métricas para obter insights sobre as postagens.")

# Carrega informações sobre o app na sidebar
load_about()
