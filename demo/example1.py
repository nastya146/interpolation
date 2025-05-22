import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from src.l2_interpolation import l2_optimization_constant, l2_optimization_linear
from src.lagrange_interpolation import lagrange_interpolation_2d
from src.linear_interpolation import bilinear_interpolation


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")

    x_coords = np.loadtxt(os.path.join(data_dir, "x_coords.txt"))
    y_coords = np.loadtxt(os.path.join(data_dir, "y_coords.txt"))
    values = np.loadtxt(os.path.join(data_dir, "values.txt"))
    x_new = np.loadtxt(os.path.join(data_dir, "x_new.txt"))
    y_new = np.loadtxt(os.path.join(data_dir, "y_new.txt"))

    bilinear_result = bilinear_interpolation(x_coords, y_coords, values, x_new, y_new)
    lagrange_result = lagrange_interpolation_2d(x_coords, y_coords, values, x_new, y_new)
    l2_constant_result = l2_optimization_constant(x_coords, y_coords, values, x_new, y_new)
    l2_linear_result = l2_optimization_linear(x_coords, y_coords, values, x_new, y_new)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    x_new_, y_new_ = np.meshgrid(x_new, y_new)
    axes[0, 0].contourf(x_new_, y_new_, bilinear_result, cmap="viridis")
    axes[0, 0].set_title("Bilinear Interpolation")
    axes[0, 1].contourf(x_new_, y_new_, lagrange_result, cmap="viridis")
    axes[0, 1].set_title("Lagrange Interpolation")
    axes[1, 0].contourf(x_new_, y_new_, l2_constant_result, cmap="viridis")
    axes[1, 0].set_title("L2 Constant")
    axes[1, 1].contourf(x_new_, y_new_, l2_linear_result, cmap="viridis")
    axes[1, 1].set_title("L2 Linear")

    plots_dir = os.path.join(base_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = os.path.join(plots_dir, f"interpolation_comparison_{timestamp}.png")
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":
    main()
