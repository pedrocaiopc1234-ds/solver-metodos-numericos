"""
EDOs — Euler e Runge-Kutta 4ª Ordem
"""

import streamlit as st
import numpy as np
import pandas as pd
from core.ode import euler_method, runge_kutta_4
from utils.ui import parse_function_2d, show_result_card, plot_ode_solution

st.set_page_config(page_title="EDOs", page_icon="🌊", layout="wide")

st.title("🌊 Equações Diferenciais Ordinárias")

method = st.selectbox(
    "Selecione o método:",
    ["Euler", "Runge-Kutta 4ª Ordem"],
    help="Escolha o método para resolver dy/dt = f(t, y)"
)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    f_str = st.text_input("f(t, y) =", value="y", help="Use `t` e `y` como variáveis.")
    y0 = st.number_input("y(0) =", value=1.0, format="%.6f")
with col2:
    t0 = st.number_input("t₀:", value=0.0, format="%.6f")
    tf = st.number_input("t_final:", value=1.0, format="%.6f")

h = st.number_input("Passo h:", value=0.1, format="%.4f")

if st.button("▶️ Calcular", use_container_width=True):
    try:
        f = parse_function_2d(f_str)

        if method == "Euler":
            st.markdown("---")
            st.subheader("📉 Método de Euler")
            st.markdown(
                "Aproximação de primeira ordem: yₙ₊₁ = yₙ + h · f(tₙ, yₙ). "
                "Simples, mas pode acumular erro para passos grandes."
            )
            result = euler_method(f, y0, t0, tf, h)
            show_result_card(result, "Solução")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("y(t_final)", f"{result['y'][-1]:.6f}")
                c2.metric("Passos", len(result["t"]))
                c3.metric("Passo h", f"{h:.4f}")

                st.markdown("#### Gráfico da Solução")
                fig = plot_ode_solution(result["t"], result["y"], "Euler")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("#### Tabela de Valores")
                df = pd.DataFrame({"t": result["t"], "y": result["y"]})
                st.dataframe(df.style.format({"t": "{:.4f}", "y": "{:.6f}"}), use_container_width=True)

        else:
            st.markdown("---")
            st.subheader("🚀 Runge-Kutta 4ª Ordem")
            st.markdown(
                "Método de quarta ordem que combina 4 avaliações de f por passo para alta precisão: "
                "yₙ₊₁ = yₙ + h/6 · (k₁ + 2k₂ + 2k₃ + k₄)."
            )
            result = runge_kutta_4(f, y0, t0, tf, h)
            show_result_card(result, "Solução")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("y(t_final)", f"{result['y'][-1]:.6f}")
                c2.metric("Passos", len(result["t"]))
                c3.metric("Passo h", f"{h:.4f}")

                st.markdown("#### Gráfico da Solução")
                fig = plot_ode_solution(result["t"], result["y"], "Runge-Kutta 4ª Ordem")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("#### Tabela de Valores")
                df = pd.DataFrame({"t": result["t"], "y": result["y"]})
                st.dataframe(df.style.format({"t": "{:.4f}", "y": "{:.6f}"}), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar entrada: {e}")
