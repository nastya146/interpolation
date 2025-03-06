def lagrange_interpolation(x, y, x_new):
    y_new = []
    n = len(x)
    for xi in x_new:
      yi = 0.
      for i in range(n):          
        num = 1.
        den = 1.
        for j in range(n):
          if j != i:
              num *= (xi - x[j])
              den *= (x[i] - x[j])
        yi += y[i] * num / den     
      y_new.append(yi)                
    return y_new
