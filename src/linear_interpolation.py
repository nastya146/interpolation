import numpy as np


def linear_interpolation(x: list, y: list, x_new: list) -> list:
    """1D билинейная интерполяция"""
    y_new = []
    for xi in x_new:
        for i in range(len(x) - 1):
            if x[i] <= xi and xi <= x[i + 1]:
                yi = y[i] + (y[i + 1] - y[i]) / (x[i + 1] - x[i]) * (xi - x[i])
                y_new.append(yi)
                break
    return y_new


def bilinear_interpolation(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    values: np.ndarray,
    x_new: np.ndarray,
    y_new: np.ndarray,
) -> np.ndarray:
    """2D билинейная интерполяция на прямоугольной сетки.

    Параметры
    ----------
    x_coords : np.ndarray
        1D массив x-координаты исходной сетки
    y_coords : np.ndarray
        1D массив y-координаты исходной сетки
    values : np.ndarray
        2D массив : значения функций на исходной сетке (len(y_coords) x len(x_coords)).
    x_new : np.ndarray
        1D массив of x-координаты новой сетки
    y_new : np.ndarray
        1D массив of y-координаты новой сетки

    Returns
    -------
    result : np.ndarray
        2D массив : значения функций на новой сетке (len(y_new) x len(x_new)).

    """
    if not isinstance(values, np.ndarray):
        values = np.array(values)
    if values.shape != (len(y_coords), len(x_coords)):
        raise ValueError(
            f"Values shape must match grid dimensions ({len(y_coords)} x {len(x_coords)})"
        )

    # проверка на уникальность значений
    x_coords = np.sort(np.unique(x_coords))
    y_coords = np.sort(np.unique(y_coords))
    if len(x_coords) < 2 or len(y_coords) < 2:
        raise ValueError("Grid must have at least 2 unique points in each dimension")

    result = np.zeros((len(y_new), len(x_new)))

    for i, y in enumerate(y_new):
        for j, x in enumerate(x_new):
            # находим ближайшие точки сетки
            i_x0 = np.searchsorted(x_coords, x, side="right") - 1
            i_x1 = min(i_x0 + 1, len(x_coords) - 1)
            i_y0 = np.searchsorted(y_coords, y, side="right") - 1
            i_y1 = min(i_y0 + 1, len(y_coords) - 1)

            x1, x2 = x_coords[i_x0], x_coords[i_x1]
            y1, y2 = y_coords[i_y0], y_coords[i_y1]

            f11 = values[i_y0, i_x0]
            f12 = values[i_y0, i_x1]
            f21 = values[i_y1, i_x0]
            f22 = values[i_y1, i_x1]

            den = (x2 - x1) * (y2 - y1)
            if abs(den) < 1e-10:  # если разность ноль
                result[i, j] = f11
            else:
                sum11 = f11 * (x2 - x) * (y2 - y) / den
                sum21 = f21 * (x - x1) * (y2 - y) / den
                sum12 = f12 * (x2 - x) * (y - y1) / den
                sum22 = f22 * (x - x1) * (y - y1) / den
                result[i, j] = sum11 + sum12 + sum21 + sum22

    return result
