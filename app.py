"""
Numerical Methods Solver — Streamlit App
======================================
Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Solver de Métodos Numéricos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Solver de Métodos Numéricos")
st.markdown("---")

cols = st.columns(3)

with cols[0]:
    st.markdown("""
    ### 🎯 Raízes
    Encontre zeros de funções reais com:
    - **Bissecção**
    - **Newton-Raphson**
    - **Secante**
    """)

with cols[1]:
    st.markdown("""
    ### 📐 Sistemas Lineares
    Resolva sistemas Ax = b com:
    - **Fatoração LU**
    - **Eliminação de Gauss**
    - **Gauss-Seidel** (iterativo)
    - **Gauss-Jacobi** (iterativo)
    """)

with cols[2]:
    st.markdown("""
    ### 📈 Interpolação
    Aproxime funções por polinômios com:
    - **Newton** (diferenças divididas)
    - **Lagrange** (polinômios base)
    """)

cols2 = st.columns(3)

with cols2[0]:
    st.markdown("""
    ### 📉 Integração
    Calcule integrais definidas com:
    - **Simpson 1/3**
    - **Trapézio Repetido**
    - **Simpson 3/8**
    """)

with cols2[1]:
    st.markdown("""
    ### 🌊 EDOs
    Resolva equações diferenciais com:
    - **Euler**
    - **Runge-Kutta 4ª ordem**
    """)

with cols2[2]:
    st.markdown("""
    ### ✨ Recursos
    - Visualizações interativas com **Plotly**
    - Tabelas de iterações detalhadas
    - Informações sobre polinômios interpoladores
    - Gráficos de convergência e áreas
    """)

st.markdown("---")
st.info("👈 Selecione um método no menu lateral para começar.")
