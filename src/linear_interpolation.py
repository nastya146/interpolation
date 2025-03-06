def linear_interpolation(x, y, x_new):
    y_new = []
    for xi in x_new:
        for i in range(len(x) - 1):
            if x[i] <= xi and xi <= x[i + 1]:
                yi = y[i] + (y[i + 1] - y[i]) / (x[i + 1] - x[i]) * (xi - x[i])
                y_new.append(yi)
                break
    return y_new