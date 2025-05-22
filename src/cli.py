import os
from datetime import datetime

import click
import numpy as np

from .l2_interpolation import l2_optimization_constant, l2_optimization_linear
from .lagrange_interpolation import lagrange_interpolation_2d
from .linear_interpolation import bilinear_interpolation


@click.group()
def cli():
    """CLI для алгоритмов 2D интерполяции"""
    pass


@cli.command()
@click.option(
    "--x-coords",
    default="data/x_coords.txt",
    type=click.Path(exists=True),
    help="Path to x-coordinates file (old grid)",
)
@click.option(
    "--y-coords",
    default="data/y_coords.txt",
    type=click.Path(exists=True),
    help="Path to y-coordinates file (old grid)",
)
@click.option(
    "--values",
    default="data/values.txt",
    type=click.Path(exists=True),
    help="Path to values file (2D array)",
)
@click.option(
    "--x-new",
    default="data/x_new.txt",
    type=click.Path(exists=True),
    help="Path to x-coordinates file (new grid)",
)
@click.option(
    "--y-new",
    default="data/y_new.txt",
    type=click.Path(exists=True),
    help="Path to y-coordinates file (new grid)",
)
@click.option(
    "--output",
    default=None,
    type=click.Path(),
    help="Path to output file for interpolated values (default: results/output_<timestamp>.txt)",
)
@click.option(
    "--algorithm",
    type=click.Choice(["bilinear", "lagrange", "l2_constant", "l2_linear"]),
    default="bilinear",
    help="Interpolation algorithm",
)
def interpolate(x_coords, y_coords, values, x_new, y_new, output, algorithm):
    """Вызов 2D интерполяции для набора точек"""
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output = os.path.join("results", f"output_{timestamp}.txt")

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    x_coords_data = np.loadtxt(x_coords)
    y_coords_data = np.loadtxt(y_coords)
    values_data = np.loadtxt(values)
    x_new_data = np.loadtxt(x_new)
    y_new_data = np.loadtxt(y_new)

    if algorithm == "bilinear":
        result = bilinear_interpolation(
            x_coords_data, y_coords_data, values_data, x_new_data, y_new_data
        )
    elif algorithm == "lagrange":
        result = lagrange_interpolation_2d(
            x_coords_data, y_coords_data, values_data, x_new_data, y_new_data
        )
    elif algorithm == "l2_constant":
        result = l2_optimization_constant(
            x_coords_data, y_coords_data, values_data, x_new_data, y_new_data
        )
    else:  # l2_linear
        result = l2_optimization_linear(
            x_coords_data, y_coords_data, values_data, x_new_data, y_new_data
        )

    # Save results
    np.savetxt(output, result, fmt="%.6f")
    click.echo(f"Interpolation completed. Results saved to {output}")
    return result


if __name__ == "__main__":
    cli()
