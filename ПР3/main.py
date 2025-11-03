import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special as sp
from scipy.optimize import minimize
from scipy import stats, signal, interpolate

# ЗАДАНИЕ 1. Работа со специальными функциями
# 1. Вычислите значения функций Бесселя первого рода J0(x) и J1(x)
#    для x от 0 до 10 с шагом 0.1
# 2. Постройте графики этих функций на одном рисунке
# 3. Найдите корни функции J0(x) на отрезке [0, 10]

x = np.arange(0, 10.1, 0.1)
J0 = sp.j0(x)
J1 = sp.j1(x)

# Нахождение корней функции J0(x) на [0, 10]
roots = sp.jn_zeros(0, 10)
print("Корни функции J0(x) на [0, 10]:", roots)

plt.figure()
plt.plot(x, J0, label="J0(x)")
plt.plot(x, J1, label="J1(x)")
plt.title("Функции Бесселя первого рода J0(x) и J1(x)")
plt.xlabel("x")
plt.ylabel("Значение функции")
plt.legend()
plt.grid(True)
plt.show()


# ЗАДАНИЕ 2. Оптимизация функции
# 1. Определите функцию f(x) = x² + 5*sin(x)
# 2. Найдите минимум этой функции на отрезке [-5, 5]
# 3. Постройте график функции и отметьте найденную точку минимума

def f(x):
    return x**2 + 5*np.sin(x)

res = minimize(f, x0=0, bounds=[(-5, 5)])
xmin = res.x[0]
ymin = f(xmin)

x_vals = np.linspace(-5, 5, 400)
y_vals = f(x_vals)

print(f"Минимум функции: x = {xmin:.3f}, f(x) = {ymin:.3f}")

plt.figure()
plt.plot(x_vals, y_vals, label="f(x) = x² + 5sin(x)")
plt.scatter(xmin, ymin, color="red", label="Минимум")
plt.title("Минимизация функции f(x) = x² + 5sin(x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()


#Задание 3: Статистический анализ данных
# 1. Вычислите основные статистические характеристики:
#    - среднее значение
#    - медиану
#    - стандартное отклонение
# 2. Постройте гистограмму данных
# 3. Проверьте гипотезу о нормальном распределении данных

data = np.random.normal(170, 10, 1000)

# Основные статистические характеристики
mean_val = np.mean(data)
median_val = np.median(data)
std_val = np.std(data)

print(f"Среднее значение: {mean_val:.2f} см")
print(f"Медиана: {median_val:.2f} см")
print(f"Стандартное отклонение: {std_val:.2f} см")

# Гистограмма распределения
plt.figure()
plt.hist(data, bins=30, density=True, alpha=0.6, color="skyblue", label="Гистограмма")
x_vals = np.linspace(min(data), max(data), 200)
plt.plot(x_vals,
         stats.norm.pdf(x_vals, 170, 10),
         color="red",
         lw=2,
         label="Теоретическая плотность N(170,10)")
plt.title("Распределение роста людей")
plt.xlabel("Рост (см)")
plt.ylabel("Плотность вероятности")
plt.legend()
plt.grid(True)
plt.show()


# ЗАДАНИЕ 4. Обработка сигнала
# 1. Примените фильтр Баттерворта низких частот 4-го порядка
#    с частотой среза 30 Гц
# 2. Постройте исходный и отфильтрованный сигналы на одном графике
# 3. Вычислите спектры обоих сигналов с помощью БПФ

t = np.linspace(0, 1, 1000)
sig = np.sin(2*np.pi*10*t) + 0.5*np.sin(2*np.pi*50*t) + 0.2*np.random.randn(1000)

# Фильтр Баттерворта НЧ 4-го порядка, частота среза 30 Гц
b, a = signal.butter(4, 30/500, "low")
filtered = signal.filtfilt(b, a, sig)

plt.figure()
plt.plot(t, sig, label="Исходный сигнал")
plt.plot(t, filtered, label="Отфильтрованный сигнал", linewidth=2)
plt.title("Фильтрация сигнала Баттервортом (низкие частоты)")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)
plt.show()

# Быстрое преобразование Фурье (БПФ)
freq = np.fft.fftfreq(len(t), d=t[1]-t[0])
spectrum_orig = np.abs(np.fft.fft(sig))
spectrum_filt = np.abs(np.fft.fft(filtered))

plt.figure()
plt.plot(freq[:500], spectrum_orig[:500], label="Исходный")
plt.plot(freq[:500], spectrum_filt[:500], label="Отфильтрованный")
plt.title("Спектры сигналов до и после фильтрации")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)
plt.show()


# ЗАДАНИЕ 5. Интерполяция данных
# 1. Создайте интерполяционные функции:
#    - линейная интерполяция
#    - кубическая сплайн-интерполяция
# 2. Вычислите значения в точках x_new = [0.5, 1.5, 2.5, 3.5, 4.5]
# 3. Сравните результаты с истинными значениями y = x²

x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 16, 25])
x_new = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
true_y = x_new**2

# Линейная и кубическая интерполяции
f_linear = interpolate.interp1d(x, y, kind="linear")
f_cubic = interpolate.interp1d(x, y, kind="cubic")

y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)

plt.figure()
plt.plot(x, y, "o", label="Исходные точки")
plt.plot(x_new, y_linear, "r--", label="Линейная интерполяция")
plt.plot(x_new, y_cubic, "g-", label="Кубическая интерполяция")
plt.plot(x_new, true_y, "k:", label="Истинная зависимость y = x²")
plt.title("Сравнение методов интерполяции")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
