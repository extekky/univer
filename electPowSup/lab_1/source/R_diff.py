import matplotlib.pyplot as plt
import numpy as np

U_st = [
    -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -4, -4.5, -5,
    -5.4, -5.5, -5.5, -5.56, -5.57, -5.57, -5.58, -5.59, -5.594, -5.597
]

I_st = [
    -171.424e-9, -171.435e-9, -171.435e-9, -171.435e-9, -171.435e-9,
    -171.435e-9, -171.435e-9, -171.435e-9, -171.435e-9, -171.436e-9,
    -31.338e-6, -461.63e-6, -943.146e-6, -1.432e-3, -1.925e-3,
    -2.419e-3, -2.914e-3, -3.41e-3, -3.906e-3, -4.403e-3
]

# Вычисление дифференциального сопротивления
R_diff = []
for i in range(1, len(U_st)):
    dU = U_st[i] - U_st[i-1]
    dI = I_st[i] - I_st[i-1]
    if dI != 0:
        R = dU / dI
    else:
        R = np.inf  # Если ток не меняется
    R_diff.append(R)

# Усредненные напряжения для сопоставления с R_diff
U_avg = [(U_st[i] + U_st[i-1])/2 for i in range(1, len(U_st))]

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(U_avg, R_diff, marker='o', linestyle='-', color='red')
plt.yscale('log')  # Логарифмическая шкала для наглядности

# Настройки графика
plt.title("Дифференциальное сопротивление R дифф", fontsize=14)
plt.xlabel("Напряжение, В", fontsize=12)
plt.ylabel("R дифф, Ом", fontsize=12)
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.axvline(x=-5.4, color="grey", linestyle="--", label="Начало пробоя")
plt.legend()
plt.show()

# Вывод результатов в табличной форме
print("| Напряжение (среднее) | R_дифф (Ом)   |")
print("|----------------------|---------------|")
for U, R in zip(U_avg, R_diff):
    print(f"| {U:8.3f}           | {R:12.2e} |")