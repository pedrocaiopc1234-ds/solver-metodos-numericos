"""
Integração Numérica — Simpson 1/3, Trapézio Repetido, Simpson 3/8
"""

import streamlit as st
import numpy as np
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from core.plot import plot_simpson, plot_trapezoidal, plot_three_eight
from utils.ui import parse_function, show_result_card

st.set_page_config(page_title="Integração", page_icon="📉", layout="wide")

st.title("📉 Integração Numérica")

method = st.selectbox(
    "Selecione o método:",
    ["Simpson 1/3", "Trapézio Repetido", "Simpson 3/8"],
    help="Escolha o método para calcular integrais definidas"
)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    f_str = st.text_input("f(x) =", value="x**2", help="Função a integrar.")
    a = st.number_input("a (limite inferior):", value=0.0, format="%.6f")
with col2:
    b = st.number_input("b (limite superior):", value=2.0, format="%.6f")

if method in ["Simpson 1/3", "Trapézio Repetido"]:
    n = st.number_input("n (número de subintervalos):", value=4, step=2 if method == "Simpson 1/3" else 1)
    if method == "Simpson 1/3" and int(n) % 2 != 0:
        st.warning("Para Simpson 1/3, n deve ser par. O cálculo irá falhar se n for ímpar.")
else:
    n = 3

if st.button("▶️ Calcular", use_container_width=True):
    try:
        f = parse_function(f_str)

        if method == "Simpson 1/3":
            st.markdown("---")
            st.subheader("🔷 Regra de Simpson 1/3")
            st.markdown(
                "Aproxima a integral usando arcos parabólicos sobre pares de subintervalos. "
                "**Fórmula:** ∫f(x)dx ≈ h/3 · [f(x₀) + 4Σf(xᵢmpar) + 2Σf(xᵢpar) + f(xₙ)]"
            )
            result = simpson(f, a, b, int(n))
            show_result_card(result, "Integral")

            if result["success"]:
                c1, c2 = st.columns(2)
                c1.metric("Integral aproximada", f"{result['result']:.10f}")
                c2.metric("n (subintervalos)", int(n))

                st.markdown("#### Gráfico com Áreas Parabólicas")
                fig = plot_simpson(f, a, b, int(n), result["result"])
                st.plotly_chart(fig, use_container_width=True)

        elif method == "Trapézio Repetido":
            st.markdown("---")
            st.subheader("🔶 Regra do Trapézio Repetido")
            st.markdown(
                "Aproxima a integral somando as áreas de trapézios formados entre pontos consecutivos. "
                "**Fórmula:** ∫f(x)dx ≈ h · [f(x₀)/2 + Σf(xᵢ) + f(xₙ)/2]"
            )
            result = trapezoidal_repeated(f, a, b, int(n))
            show_result_card(result, "Integral")

            if result["success"]:
                c1, c2 = st.columns(2)
                c1.metric("Integral aproximada", f"{result['result']:.10f}")
                c2.metric("n (subintervalos)", int(n))

                st.markdown("#### Gráfico com Trapézios")
                fig = plot_trapezoidal(f, a, b, int(n), result["result"])
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.markdown("---")
            st.subheader("🔸 Regra de Simpson 3/8")
            st.markdown(
                "Aproxima a integral usando polinômios cúbicos sobre 3 subintervalos (4 pontos). "
                "**Fórmula:** ∫f(x)dx ≈ 3h/8 · [f(x₀) + 3f(x₁) + 3f(x₂) + f(x₃)]"
            )
            result = three_eight_method(f, a, b)
            show_result_card(result, "Integral")

            if result["success"]:
                c1, c2 = st.columns(2)
                c1.metric("Integral aproximada", f"{result['result']:.10f}")
                c2.metric("n (subintervalos)", 3)

                st.markdown("#### Gráfico com Área Cúbica")
                fig = plot_three_eight(f, a, b, result["result"])
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar entrada: {e}")
