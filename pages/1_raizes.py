"""
Métodos para Encontrar Raízes — Bissecção, Newton-Raphson, Secante
"""

import streamlit as st
import numpy as np
import pandas as pd
from core.roots import bisection, newton, secant
from core.plot import plot_bisection, plot_newton, plot_secant
from utils.ui import parse_function, show_result_card

st.set_page_config(page_title="Raízes", page_icon="🎯", layout="wide")

st.title("🎯 Métodos para Encontrar Raízes")

method = st.selectbox(
    "Selecione o método:",
    ["Bissecção", "Newton-Raphson", "Secante"],
    help="Escolha o método numérico para encontrar raízes de f(x)=0"
)

st.markdown("---")

if method == "Bissecção":
    st.subheader("📐 Método da Bissecção")
    st.markdown(
        "O método da bissecção divide o intervalo `[a, b]` ao meio repetidamente "
        "até que a raiz seja encontrada com a tolerância desejada. "
        "**Requisito:** `f(a)` e `f(b)` devem ter sinais opostos."
    )

    col1, col2 = st.columns(2)
    with col1:
        f_str = st.text_input("f(x) =", value="x**2 - 4", help="Expressão da função. Use `x` como variável.")
        a = st.number_input("a (início do intervalo):", value=0.0, format="%.6f")
    with col2:
        b = st.number_input("b (fim do intervalo):", value=3.0, format="%.6f")
        tol = st.number_input("Tolerância:", value=1e-6, format="%.2e")
    max_iter = st.slider("Máximo de iterações:", 10, 500, 100)

    if st.button("▶️ Calcular", use_container_width=True):
        try:
            f = parse_function(f_str)
            fa, fb = f(a), f(b)

            col_info = st.columns(3)
            col_info[0].metric("f(a)", f"{fa:.6f}")
            col_info[1].metric("f(b)", f"{fb:.6f}")
            col_info[2].metric("Sinal", "OK ✅" if fa * fb <= 0 else "Inválido ❌")

            result = bisection(f, a, b, tol, max_iter)
            show_result_card(result, "Raiz")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Raiz aproximada", f"{result['root']:.10f}")
                c2.metric("Iterações", result["iterations"])
                c3.metric("f(raiz)", f"{f(result['root']):.2e}")

                st.markdown("#### Gráfico")
                fig = plot_bisection(f, a, b, result["root"], result["iterations"])
                st.plotly_chart(fig, use_container_width=True)

                if result.get("iterations_data"):
                    st.markdown("#### Tabela de Iterações")
                    df = pd.DataFrame(result["iterations_data"])
                    df.index = df.index + 1
                    df.index.name = "Iteração"
                    st.dataframe(df.style.format({"a": "{:.8f}", "b": "{:.8f}", "c": "{:.8f}", "fc": "{:.2e}"}), use_container_width=True)
            else:
                if result.get("iterations_data"):
                    st.markdown("#### Últimas Iterações")
                    df = pd.DataFrame(result["iterations_data"])
                    df.index = df.index + 1
                    df.index.name = "Iteração"
                    st.dataframe(df.style.format({"a": "{:.8f}", "b": "{:.8f}", "c": "{:.8f}", "fc": "{:.2e}"}), use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao processar entrada: {e}")

elif method == "Newton-Raphson":
    st.subheader("🔥 Método de Newton-Raphson")
    st.markdown(
        "O método de Newton usa a derivada da função para aproximar a raiz de forma iterativa. "
        "Converge rapidamente quando o chute inicial está próximo da raiz. "
        "**Requisito:** você precisa informar `f(x)` e `f'(x)`."
    )

    col1, col2 = st.columns(2)
    with col1:
        f_str = st.text_input("f(x) =", value="x**2 - 4", help="Expressão da função.")
        df_str = st.text_input("f'(x) =", value="2*x", help="Expressão da derivada.")
    with col2:
        x0 = st.number_input("Chute inicial x₀:", value=3.0, format="%.6f")
        tol = st.number_input("Tolerância:", value=1e-6, format="%.2e")
    max_iter = st.slider("Máximo de iterações:", 10, 500, 100)

    if st.button("▶️ Calcular", use_container_width=True):
        try:
            f = parse_function(f_str)
            df = parse_function(df_str)
            result = newton(f, df, x0, tol, max_iter)
            show_result_card(result, "Raiz")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Raiz aproximada", f"{result['root']:.10f}")
                c2.metric("Iterações", result["iterations"])
                c3.metric("f(raiz)", f"{f(result['root']):.2e}")

                st.markdown("#### Gráfico com Tangentes")
                fig = plot_newton(f, df, x0, result["root"], result.get("iterations_data"))
                st.plotly_chart(fig, use_container_width=True)

                if result.get("iterations_data"):
                    st.markdown("#### Tabela de Iterações")
                    df_iter = pd.DataFrame(result["iterations_data"])
                    df_iter.index = df_iter.index + 1
                    df_iter.index.name = "Iteração"
                    st.dataframe(
                        df_iter.style.format({
                            "x": "{:.8f}", "fx": "{:.2e}", "dfx": "{:.6f}", "x_next": "{:.8f}"
                        }),
                        use_container_width=True
                    )
            else:
                if result.get("iterations_data"):
                    st.markdown("#### Últimas Iterações")
                    df_iter = pd.DataFrame(result["iterations_data"])
                    df_iter.index = df_iter.index + 1
                    df_iter.index.name = "Iteração"
                    st.dataframe(
                        df_iter.style.format({
                            "x": "{:.8f}", "fx": "{:.2e}", "dfx": "{:.6f}", "x_next": "{:.8f}"
                        }),
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"Erro ao processar entrada: {e}")

else:
    st.subheader("📏 Método da Secante")
    st.markdown(
        "O método da secante aproxima a derivada usando dois pontos consecutivos, "
        "evitando a necessidade de calcular a derivada analítica. "
        "**Requisito:** dois chutes iniciais `x₀` e `x₁`."
    )

    col1, col2 = st.columns(2)
    with col1:
        f_str = st.text_input("f(x) =", value="x**2 - 4", help="Expressão da função.")
        x0 = st.number_input("x₀:", value=0.0, format="%.6f")
    with col2:
        x1 = st.number_input("x₁:", value=3.0, format="%.6f")
        tol = st.number_input("Tolerância:", value=1e-6, format="%.2e")
    max_iter = st.slider("Máximo de iterações:", 10, 500, 100)

    if st.button("▶️ Calcular", use_container_width=True):
        try:
            f = parse_function(f_str)
            result = secant(f, x0, x1, tol, max_iter)
            show_result_card(result, "Raiz")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Raiz aproximada", f"{result['root']:.10f}")
                c2.metric("Iterações", result["iterations"])
                c3.metric("f(raiz)", f"{f(result['root']):.2e}")

                st.markdown("#### Gráfico com Secantes")
                fig = plot_secant(f, x0, x1, result["root"], result.get("iterations_data"))
                st.plotly_chart(fig, use_container_width=True)

                if result.get("iterations_data"):
                    st.markdown("#### Tabela de Iterações")
                    df_iter = pd.DataFrame(result["iterations_data"])
                    df_iter.index = df_iter.index + 1
                    df_iter.index.name = "Iteração"
                    st.dataframe(
                        df_iter.style.format({
                            "x0": "{:.8f}", "x1": "{:.8f}",
                            "f0": "{:.2e}", "f1": "{:.2e}", "x2": "{:.8f}"
                        }),
                        use_container_width=True
                    )
            else:
                if result.get("iterations_data"):
                    st.markdown("#### Últimas Iterações")
                    df_iter = pd.DataFrame(result["iterations_data"])
                    df_iter.index = df_iter.index + 1
                    df_iter.index.name = "Iteração"
                    st.dataframe(
                        df_iter.style.format({
                            "x0": "{:.8f}", "x1": "{:.8f}",
                            "f0": "{:.2e}", "f1": "{:.2e}", "x2": "{:.8f}"
                        }),
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"Erro ao processar entrada: {e}")
