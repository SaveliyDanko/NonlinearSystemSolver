def show_main_menu():
    """
    Отображает главное меню и возвращает выбранный пункт.
    """
    print("Выберите действие:")
    print("1) Нелинейное уравнение")
    print("2) Система нелинейных уравнений")
    print("3) Выход")

    choice = input("Введите номер пункта: ").strip()
    return choice
