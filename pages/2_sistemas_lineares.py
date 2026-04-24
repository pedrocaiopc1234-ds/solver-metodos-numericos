"""
Sistemas Lineares — LU, Gauss, Gauss-Seidel, Gauss-Jacobi
"""

import streamlit as st
import numpy as np
import pandas as pd
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
from utils.ui import display_matrix, show_result_card

st.set_page_config(page_title="Sistemas Lineares", page_icon="📐", layout="wide")

st.title("📐 Sistemas Lineares")

method = st.selectbox(
    "Selecione o método:",
    ["Fatoração LU", "Eliminação de Gauss", "Gauss-Seidel", "Gauss-Jacobi"],
    help="Escolha o método para resolver Ax = b"
)

st.markdown("---")

st.markdown("**Entrada da Matriz A e Vetor b**")
A_str = st.text_area(
    "Matriz A (linhas separadas por `;`, valores por `,`):",
    value="4, 1, 2\n1, 3, 1\n2, 1, 5",
    height=120,
    help="Exemplo para matriz 3x3: `4, 1, 2; 1, 3, 1; 2, 1, 5`"
)
b_str = st.text_input("Vetor b (valores separados por `,`):", value="4, 3, 7")

if method in ["Gauss-Seidel", "Gauss-Jacobi"]:
    col_iter = st.columns(3)
    with col_iter[0]:
        tol = st.number_input("Tolerância:", value=1e-10, format="%.2e")
    with col_iter[1]:
        max_iter = st.number_input("Máximo de iterações:", value=100, step=10)
else:
    tol = 1e-10
    max_iter = 100

if st.button("▶️ Calcular", use_container_width=True):
    try:
        A = np.array([[float(x.strip()) for x in row.split(",")] for row in A_str.strip().splitlines() if row.strip()])
        b = np.array([float(x.strip()) for x in b_str.split(",")])

        st.markdown("### Entrada Validada")
        c1, c2 = st.columns(2)
        with c1:
            display_matrix(A, "Matriz A")
        with c2:
            display_matrix(b.reshape(-1, 1), "Vetor b")

        if method == "Fatoração LU":
            st.markdown("---")
            st.subheader("🔢 Fatoração LU com Pivotamento Parcial")
            st.markdown(
                "Decompõe a matriz A em A = LU, onde L é triangular inferior e U é triangular superior. "
                "Em seguida, resolve o sistema por substituição."
            )
            result = lu_factorization(A, b)
            show_result_card(result, "Solução")

            if result["success"]:
                c1, c2 = st.columns(2)
                with c1:
                    display_matrix(result["L"], "Matriz L (inferior)")
                with c2:
                    display_matrix(result["U"], "Matriz U (superior)")

                st.markdown("**Solução x:**")
                display_matrix(result["x"].reshape(-1, 1), "x")

                st.markdown("**Verificação (A @ x):**")
                Ax = np.dot(A, result["x"])
                display_matrix(Ax.reshape(-1, 1), "A · x")
                st.markdown(f"**Erro ||Ax - b||₂:** {np.linalg.norm(Ax - b):.2e}")

        elif method == "Eliminação de Gauss":
            st.markdown("---")
            st.subheader("🔢 Eliminação de Gauss com Pivotamento Parcial")
            st.markdown(
                "Transforma a matriz aumentada [A|b] em uma forma triangular superior por operações elementares, "
                "e depois resolve por retrosubstituição."
            )
            result = gaussian_elimination(A, b)
            show_result_card(result, "Solução")

            if result["success"]:
                display_matrix(result["x"].reshape(-1, 1), "Solução x")

                st.markdown("**Verificação (A @ x):**")
                Ax = np.dot(A, result["x"])
                display_matrix(Ax.reshape(-1, 1), "A · x")
                st.markdown(f"**Erro ||Ax - b||₂:** {np.linalg.norm(Ax - b):.2e}")

        elif method == "Gauss-Seidel":
            st.markdown("---")
            st.subheader("🔁 Gauss-Seidel (Método Iterativo)")
            st.markdown(
                "Atualiza cada componente de x usando os valores **já atualizados** da iteração corrente. "
                "Converge se A for diagonalmente dominante ou simétrica definida positiva."
            )
            result = gauss_seidel(A, b, tol=tol, max_iter=max_iter)
            show_result_card(result, "Solução")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Iterações", result["iterations"])
                c2.metric("Tolerância", f"{tol:.2e}")
                c3.metric("Convergiu", "Sim ✅")

                display_matrix(result["x"].reshape(-1, 1), "Solução x")

                st.markdown("**Verificação (A @ x):**")
                Ax = np.dot(A, result["x"])
                display_matrix(Ax.reshape(-1, 1), "A · x")
                st.markdown(f"**Erro ||Ax - b||₂:** {np.linalg.norm(Ax - b):.2e}")

        else:
            st.markdown("---")
            st.subheader("🔁 Gauss-Jacobi (Método Iterativo)")
            st.markdown(
                "Atualiza cada componente de x usando os valores **da iteração anterior**. "
                "Converge se A for diagonalmente dominante."
            )
            result = gauss_jacobi(A, b, tol=tol, max_iter=max_iter)
            show_result_card(result, "Solução")

            if result["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Iterações", result["iterations"])
                c2.metric("Tolerância", f"{tol:.2e}")
                c3.metric("Convergiu", "Sim ✅")

                display_matrix(result["x"].reshape(-1, 1), "Solução x")

                st.markdown("**Verificação (A @ x):**")
                Ax = np.dot(A, result["x"])
                display_matrix(Ax.reshape(-1, 1), "A · x")
                st.markdown(f"**Erro ||Ax - b||₂:** {np.linalg.norm(Ax - b):.2e}")

    except Exception as e:
        st.error(f"Erro ao processar entrada: {e}")
