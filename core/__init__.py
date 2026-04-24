from core.roots import bisection, newton, secant
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
from core.interpolation import newton_interpolation, lagrange_interpolation
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from core.ode import euler_method, runge_kutta_4
from core.plot import (
    plot_bisection,
    plot_newton,
    plot_secant,
    plot_newton_interpolation,
    plot_lagrange_interpolation,
    plot_simpson,
    plot_trapezoidal,
    plot_three_eight,
)
