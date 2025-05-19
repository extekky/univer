import matplotlib.pyplot as plt

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

# Построение графика
plt.figure(figsize=(12, 7))
plt.plot(U_st, I_st, marker='o', linestyle='-', color='blue', markersize=6)

# Настройка оформления
plt.title("Вольт-амперная характеристика", fontsize=14)
plt.xlabel("Напряжение, В", fontsize=12)
plt.ylabel("Ток, А", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)

# Форматирование осей (научная нотация для тока)
plt.ticklabel_format(axis="y", style="sci", scilimits=(-3, 3))

# Выделение области пробоя (опционально)
plt.axvline(x=-5.4, color="red", linestyle="--", alpha=0.5, label="Начало пробоя")
plt.legend()

plt.show()