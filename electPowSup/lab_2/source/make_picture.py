import matplotlib.pyplot as plt

E_б = [0.7, 1.5, 2.5, 3.5, 4.5]
E_э = [0.0, 0.8, 1.8, 2.8, 3.8]
E_к = [10.0, 9.8, 9.2, 8.2, 7.2]

plt.plot(E_б, E_э, label='Eэ = f(Eб)')
plt.plot(E_б, E_к, label='Eк = f(Eб)')
plt.xlabel('Eб (В)')
plt.ylabel('Напряжение (В)')
plt.legend()
plt.grid(True)
plt.show()