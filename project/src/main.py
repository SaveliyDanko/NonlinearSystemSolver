from menu import show_main_menu
from data_equations import NONLINEAR_EQUATIONS, NONLINEAR_SYSTEMS
from input_handler import choose_nonlinear_equation, choose_nonlinear_system
from methods_menu import show_nonlinear_equation_methods, show_nonlinear_system_methods

# Импортируем сами методы
from methods.nonlinear_equations import chord_method, newton_method, iteration_method as iteration_eq
from methods.nonlinear_systems import iteration_method as iteration_sys

# Дополнительные импорты для отрисовки графиков
import matplotlib.pyplot as plt
import numpy as np
import sympy
import math


import sympy
import numpy as np
import matplotlib.pyplot as plt


def parse_equation(eq_str):
    eq_str = eq_str.replace('^', '**')
    eq_str = eq_str.replace('= 0', '')
    return eq_str.strip()


def plot_nonlinear_equation(equation_str):
    eq_clean = parse_equation(equation_str)
    x = sympy.symbols('x')

    try:
        expr = sympy.sympify(eq_clean)
    except sympy.SympifyError as e:
        print(f"Не удалось преобразовать уравнение для построения графика: {e}")
        return

    f = sympy.lambdify(x, expr, 'numpy')

    x_vals = np.linspace(-10, 10, 400)
    try:
        y_vals = f(x_vals)
    except Exception as e:
        print(f"Ошибка при вычислении значений функции: {e}")
        return

    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f"f(x) = {eq_clean}")
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title("График нелинейного уравнения")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("equation_plot.png")
    plt.close()
    print("График уравнения сохранён в файл: equation_plot.png")


def plot_nonlinear_system(system):
    if len(system) < 2:
        print("Система должна содержать минимум 2 уравнения.")
        return

    x_sym, y_sym = sympy.symbols('x y')
    funcs = []
    labels = []

    for eq in system:
        eq_clean = parse_equation(eq)
        try:
            expr = sympy.sympify(eq_clean)
            func = sympy.lambdify((x_sym, y_sym), expr, 'numpy')
            funcs.append(func)
            labels.append(eq_clean)
        except sympy.SympifyError as e:
            print(f"Ошибка при обработке '{eq}': {e}")
            return

    x_vals = np.linspace(-5, 5, 400)
    y_vals = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x_vals, y_vals)

    plt.figure(figsize=(8, 6))
    for func, label in zip(funcs, labels):
        try:
            Z = func(X, Y)
            contour = plt.contour(X, Y, Z, levels=[0], linewidths=2)
            plt.clabel(contour, fmt={0: label}, inline=True, fontsize=9)
        except Exception as e:
            print(f"Ошибка при вычислении значений для {label}: {e}")
            return

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("График системы нелинейных уравнений")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("system_plot.png")
    plt.close()
    print("График системы сохранён в файл: system_plot.png")



def main():
    while True:
        choice = show_main_menu()

        if choice == '1':
            # Пользователь выбрал "Нелинейное уравнение"
            selected_equation = choose_nonlinear_equation(NONLINEAR_EQUATIONS)
            if selected_equation is None:
                print("Возвращаемся в главное меню...\n")
                continue

            # Отрисовываем график выбранного уравнения
            plot_nonlinear_equation(selected_equation)

            # Покажем меню выбора метода для нелинейного уравнения
            method_choice = show_nonlinear_equation_methods()
            if method_choice is None:
                print("Возвращаемся в главное меню...\n")
                continue

            # Вызываем соответствующий метод
            if method_choice == '1':
                chord_method(selected_equation)
            elif method_choice == '2':
                newton_method(selected_equation)
            elif method_choice == '3':
                iteration_eq(selected_equation)
            else:
                print("Некорректный метод. Возвращаемся в главное меню...\n")

        elif choice == '2':
            # Пользователь выбрал "Система нелинейных уравнений"
            selected_system = choose_nonlinear_system(NONLINEAR_SYSTEMS)
            if selected_system is None:
                print("Возвращаемся в главное меню...\n")
                continue

            # Отрисовываем график выбранной системы
            plot_nonlinear_system(selected_system)

            # Покажем меню выбора метода (для систем - пока один метод)
            method_choice = show_nonlinear_system_methods()
            if method_choice is None:
                print("Возвращаемся в главное меню...\n")
                continue

            # Вызываем соответствующий метод
            if method_choice == '1':
                iteration_sys(selected_system)
            else:
                print("Некорректный метод. Возвращаемся в главное меню...\n")

        elif choice == '3':
            # Пользователь выбрал "Выход"
            print("Выход из программы...")
            break

        else:
            print("Некорректный пункт меню. Пожалуйста, выберите 1, 2 или 3.\n")


if __name__ == "__main__":
    main()
