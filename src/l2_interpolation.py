import numpy as np


def l2_optimization_constant(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    values: np.ndarray,
    x_new: np.ndarray,
    y_new: np.ndarray,
) -> np.ndarray:
    """
    L2-optimal interpolation between two grids with constant basis functions,
    returning values at nodes of the new grid.

    Args:
        x_coords: 1D array of x-coordinates of the original grid.
        y_coords: 1D array of y-coordinates of the original grid.
        values: 2D array of values on the original grid.
        x_new: 1D array of x-coordinates of the new grid.
        y_new: 1D array of y-coordinates of the new grid.

    Returns:
        2D array of interpolated values at nodes of the new grid, shape (len(y_new), len(x_new)).
    """
    # Initialize result array for new grid nodes
    result = np.zeros((len(y_new), len(x_new)))

    # Iterate over new grid nodes
    for i in range(len(x_new)):
        for j in range(len(y_new)):
            x_n = x_new[i]
            y_n = y_new[j]

            weighted_sum = 0.0
            total_weight = 0.0

            # Iterate over original grid cells
            for m in range(len(x_coords) - 1):
                for n in range(len(y_coords) - 1):
                    # Define original cell boundaries
                    x0_orig, x1_orig = x_coords[m], x_coords[m + 1]
                    y0_orig, y1_orig = y_coords[n], y_coords[n + 1]

                    # Define influence area around the new node (e.g., a small rectangle)
                    # For simplicity, use a small fixed radius or grid-based influence
                    delta_x = (
                        min(np.diff(x_new).mean() / 2, np.diff(x_coords).mean() / 2)
                        if len(x_new) > 1
                        else 1.0
                    )
                    delta_y = (
                        min(np.diff(y_new).mean() / 2, np.diff(y_coords).mean() / 2)
                        if len(y_new) > 1
                        else 1.0
                    )
                    x0_influence = x_n - delta_x
                    x1_influence = x_n + delta_x
                    y0_influence = y_n - delta_y
                    y1_influence = y_n + delta_y

                    # Find intersection with original cell
                    x_intersect_left = max(x0_influence, x0_orig)
                    x_intersect_right = min(x1_influence, x1_orig)
                    y_intersect_top = max(y0_influence, y0_orig)
                    y_intersect_bottom = min(y1_influence, y1_orig)

                    # Calculate intersection area
                    intersect_width = max(0, x_intersect_right - x_intersect_left)
                    intersect_height = max(0, y_intersect_bottom - y_intersect_top)
                    intersect_area = intersect_width * intersect_height

                    if intersect_area > 0:
                        # Weight by intersection area
                        weight = intersect_area
                        weighted_sum += weight * values[n, m]
                        total_weight += weight

            # Compute value for the new node
            if total_weight > 0:
                result[j, i] = weighted_sum / total_weight
            else:
                result[j, i] = np.nan  # Handle cases with no overlap

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
