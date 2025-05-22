import numpy as np


def lagrange_interpolation_1d(x: np.ndarray, y: np.ndarray, x_new: np.ndarray) -> np.ndarray:
    """1D интерполяция Лагранжа"""
    y_new = np.zeros(len(x_new))
    n = len(x)
    for k, xi in enumerate(x_new):
        yi = 0.0
        for i in range(n):
            num = 1.0
            den = 1.0
            for j in range(n):
                if j != i:
                    num *= xi - x[j]
                    den *= x[i] - x[j]
            yi += y[i] * num / den
        y_new[k] = yi
    return y_new


def lagrange_interpolation_2d(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    values: np.ndarray,
    x_new: np.ndarray,
    y_new: np.ndarray,
) -> np.ndarray:
    """2D интерполяция Лагранжа на прямоугольной сетке
    (упрощенная: применяет 1D интерполяцию по каждой сетке).

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
        raise ValueError("Values shape must match grid dimensions (len(y_coords) x len(x_coords))")

    result = np.zeros((len(y_new), len(x_new)))

    # Шаг 1: Интерполяция по оси x для каждой y-координаты
    temp = np.zeros((len(y_coords), len(x_new)))
    for i in range(len(y_coords)):
        temp[i, :] = lagrange_interpolation_1d(x_coords, values[i, :], x_new)

    # Шаг 2: Интерполяция по оси y
    for j in range(len(x_new)):
        result[:, j] = lagrange_interpolation_1d(y_coords, temp[:, j], y_new)

    return result
