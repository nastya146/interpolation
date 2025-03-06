import numpy as np
import matplotlib.pyplot as plt
import os 
from datetime import datetime
from src.lagrange_interpolation import lagrange_interpolation

#Пример использования интерполяции Лагранжа
def main():
  x = np.linspace(0, 10, num=10)
  y = x * x
  x_new = np.linspace(0, 10, num=100)
  y_new = lagrange_interpolation(x, y, x_new)

  plt.plot(x, y, 'o', label='Исходные данные')
  plt.plot(x_new, y_new, '-', label='Интерполяция многочленами Лагранжа')
  plt.legend()
  timestamp = datetime.now().strftime("%Y%m%d_%H%M")
  base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
  plots_dir = os.path.join(base_dir, "plots")
  os.makedirs(plots_dir, exist_ok = True)
  filename = os.path.join(plots_dir, f"lagrange_interpolation_{timestamp}.png")
  plt.savefig(filename)

if __name__ == "__main__": main()