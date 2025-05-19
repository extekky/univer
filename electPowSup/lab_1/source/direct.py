import matplotlib.pyplot as plt

U_st = [0.560, 0.620, 0.647, 0.665, 0.679, 0.689, 0.698, 0.706, 0.712, 0.718]  # Напряжение в вольтах (В)
I_st = [0.0087, 0.027, 0.047, 0.066, 0.086, 0.106, 0.126, 0.145, 0.165, 0.185]  # Ток в амперах (А)

# Построение графика
plt.figure(figsize=(10, 6))
# plt.plot(U_st, I_st, marker='o', linestyle='-', color='b', label='ВАХ')
plt.plot(U_st, I_st, marker='o', linestyle='-', color='b', label='ВАХ')

# Настройка осей и заголовка
plt.xlabel('Напряжение, В', fontsize=12)
plt.ylabel('Ток, А', fontsize=12)
plt.title('Вольт-амперная характеристика', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Форматирование осей (опционально)
plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))

# Отображение графика
plt.show()