# main.py

from menu import show_main_menu
from data_equations import NONLINEAR_EQUATIONS, NONLINEAR_SYSTEMS
from input_handler import choose_nonlinear_equation, choose_nonlinear_system
from methods_menu import show_nonlinear_equation_methods, show_nonlinear_system_methods

# Импортируем сами методы
from methods.nonlinear_equations import chord_method, newton_method, iteration_method as iteration_eq
from methods.nonlinear_systems import iteration_method as iteration_sys


def main():
    while True:
        choice = show_main_menu()

        if choice == '1':
            # Пользователь выбрал "Нелинейное уравнение"
            selected_equation = choose_nonlinear_equation(NONLINEAR_EQUATIONS)
            if selected_equation is None:
                print("Возвращаемся в главное меню...\n")
                continue

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
