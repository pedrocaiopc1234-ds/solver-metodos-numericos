"""
Interpolação Polinomial — Newton e Lagrange
"""

import streamlit as st
import numpy as np
import pandas as pd
from core.interpolation import newton_interpolation, lagrange_interpolation
from core.plot import plot_newton_interpolation, plot_lagrange_interpolation
from utils.ui import show_result_card

st.set_page_config(page_title="Interpolação", page_icon="📈", layout="wide")

st.title("📈 Interpolação Polinomial")

method = st.selectbox(
    "Selecione o método:",
    ["Newton (Diferenças Divididas)", "Lagrange"],
    help="Escolha o método de interpolação polinomial"
)

st.markdown("---")

st.markdown("**Pontos de Interpolação**")
col1, col2 = st.columns(2)
with col1:
    x_str = st.text_input("x (separados por vírgula):", value="1, 2, 3, 4")
with col2:
    y_str = st.text_input("y (separados por vírgula):", value="1, 4, 9, 16")

x_eval = st.number_input("x a avaliar:", value=2.5, format="%.6f")

if st.button("▶️ Calcular", use_container_width=True):
    try:
        x = np.array([float(v.strip()) for v in x_str.split(",")])
        y = np.array([float(v.strip()) for v in y_str.split(",")])

        if len(x) != len(y):
            st.error("x e y devem ter o mesmo número de elementos.")
        elif len(x) < 2:
            st.error("Mínimo de 2 pontos necessários.")
        else:
            st.markdown("### Pontos de Interpolação")
            pts_df = pd.DataFrame({"x": x, "y": y})
            st.dataframe(pts_df, use_container_width=True)

            if method == "Newton (Diferenças Divididas)":
                st.markdown("---")
                st.subheader("📊 Interpolação de Newton")
                st.markdown(
                    "A interpolação de Newton utiliza **diferenças divididas** para construir o polinômio "
                    "de forma incremental, adicionando um termo a cada novo ponto."
                )

                result = newton_interpolation(x, y, x_eval)
                show_result_card(result, "Interpolação")

                if result["success"]:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("P(x) avaliado", f"{result['result']:.6f}")
                    c2.metric("Grau do polinômio", len(x) - 1)
                    c3.metric("x avaliado", f"{x_eval:.4f}")

                    fig, info = plot_newton_interpolation(
                        x, y, result["coefficients"],
                        x_eval=x_eval, y_eval=result["result"]
                    )

                    st.markdown("#### Gráfico do Polinômio Interpolador")
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("#### Informações do Polinômio")
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.markdown(f"**Base:** {info['basis']}")
                        st.markdown(f"**Forma:** `{info['form']}`")
                        st.markdown(f"**Grau:** {info['degree']}")
                    with info_col2:
                        st.markdown(f"**Coeficientes (c₀, c₁, ...):**")
                        coeffs = info["coefficients"]
                        for i, c in enumerate(coeffs):
                            st.markdown(f"- c{i} = `{c:.6g}`")

                    st.markdown("**Polinômio expandido:**")
                    st.code(info["polynomial_string"], language="text")

            else:
                st.markdown("---")
                st.subheader("📊 Interpolação de Lagrange")
                st.markdown(
                    "A interpolação de Lagrange constrói o polinômio como uma combinação linear de "
                    "**polinômios base** Lᵢ(x), cada um valendo 1 em xᵢ e 0 nos outros nós."
                )

                result = lagrange_interpolation(x, y, x_eval)
                show_result_card(result, "Interpolação")

                if result["success"]:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("P(x) avaliado", f"{result['result']:.6f}")
                    c2.metric("Grau do polinômio", len(x) - 1)
                    c3.metric("x avaliado", f"{x_eval:.4f}")

                    fig, info = plot_lagrange_interpolation(
                        x, y, x_eval=x_eval, y_eval=result["result"]
                    )

                    st.markdown("#### Gráfico do Polinômio Interpolador")
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("#### Informações do Polinômio")
                    info_col1, info_col2 = st.columns(2)
                    with info_col1:
                        st.markdown(f"**Base:** {info['basis']}")
                        st.markdown(f"**Forma:** `{info['form']}`")
                        st.markdown(f"**Grau:** {info['degree']}")
                    with info_col2:
                        st.markdown("**Polinômios base Lᵢ(x):**")
                        for s in info["basis_strings"]:
                            st.markdown(f"- `{s}`")

                    st.markdown("**Polinômio expandido:**")
                    st.code(info["polynomial_string"], language="text")

    except Exception as e:
        st.error(f"Erro ao processar entrada: {e}")
