import numpy as np


def l2_optimization_constant(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    values: np.ndarray,
    x_new: np.ndarray,
    y_new: np.ndarray,
) -> np.ndarray:
    """L2 optimization between grids with constant basis functions (placeholder).

    Parameters
    ----------
    x_coords : np.ndarray
        1D array of x-coordinates of the original grid.
    y_coords : np.ndarray
        1D array of y-coordinates of the original grid.
    values : np.ndarray
        2D array of function values on the original grid (shape: len(y_coords) x len(x_coords)).
    x_new : np.ndarray
        1D array of x-coordinates of the new grid.
    y_new : np.ndarray
        1D array of y-coordinates of the new grid.

    Returns
    -------
    result : np.ndarray
        2D array of interpolated values (placeholder: nearest neighbor).

    """
    # TODO: Implement L2 optimization for constant basis functions
    if not isinstance(values, np.ndarray):
        values = np.array(values)
    if values.shape != (len(y_coords), len(x_coords)):
        raise ValueError("Values shape must match grid dimensions")

    result = np.zeros((len(y_new), len(x_new)))
    for i, y in enumerate(y_new):
        for j, x in enumerate(x_new):
            i_x = np.searchsorted(x_coords, x, side="right") - 1
            i_y = np.searchsorted(y_coords, y, side="right") - 1
            i_x = min(i_x, len(x_coords) - 1)
            i_y = min(i_y, len(y_coords) - 1)
            result[i, j] = values[i_y, i_x]
    return result


def l2_optimization_linear(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    values: np.ndarray,
    x_new: np.ndarray,
    y_new: np.ndarray,
) -> np.ndarray:
    """L2 optimization between grids with piecewise linear functions (placeholder).

    Parameters
    ----------
    x_coords : np.ndarray
        1D array of x-coordinates of the original grid.
    y_coords : np.ndarray
        1D array of y-coordinates of the original grid.
    values : np.ndarray
        2D array of function values on the original grid (shape: len(y_coords) x len(x_coords)).
    x_new : np.ndarray
        1D array of x-coordinates of the new grid.
    y_new : np.ndarray
        1D array of y-coordinates of the new grid.

    Returns
    -------
    result : np.ndarray
        2D array of interpolated values (placeholder: bilinear interpolation).

    """
    # TODO: Implement L2 optimization for piecewise linear functions
    from .linear_interpolation import bilinear_interpolation

    return bilinear_interpolation(x_coords, y_coords, values, x_new, y_new)
