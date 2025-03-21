# input_handler.py

def choose_nonlinear_equation(equations_list):
    """
    Предлагает пользователю выбрать одно из доступных нелинейных уравнений.
    Возвращает строковое представление выбранного уравнения (или None при отмене).
    """
    print("\nДоступные нелинейные уравнения:")
    for index, equation in enumerate(equations_list, start=1):
        print(f"{index}) {equation}")

    while True:
        choice = input("Введите номер уравнения (или 'q' для отмены): ").strip()

        if choice.lower() == 'q':
            print("Отмена выбора уравнения.")
            return None

        if choice.isdigit():
            eq_num = int(choice)
            if 1 <= eq_num <= len(equations_list):
                return equations_list[eq_num - 1]

        print("Некорректный ввод. Попробуйте снова.")


def choose_nonlinear_system(systems_list):
    """
    Предлагает пользователю выбрать одну из доступных систем нелинейных уравнений.
    Возвращает список строк (уравнений), соответствующих выбранной системе (или None при отмене).
    """
    print("\nДоступные системы нелинейных уравнений:")
    for index, system in enumerate(systems_list, start=1):
        # Склеиваем уравнения системы в одну строку для упрощённого отображения
        system_str = " и ".join(system)
        print(f"{index}) {system_str}")

    while True:
        choice = input("Введите номер системы (или 'q' для отмены): ").strip()

        if choice.lower() == 'q':
            print("Отмена выбора системы.")
            return None

        if choice.isdigit():
            sys_num = int(choice)
            if 1 <= sys_num <= len(systems_list):
                return systems_list[sys_num - 1]

        print("Некорректный ввод. Попробуйте снова.")
