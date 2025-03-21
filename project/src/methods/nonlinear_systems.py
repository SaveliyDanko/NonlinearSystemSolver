import sympy
import math


def read_parameters():
    """
    Считывает параметры метода: alpha, x0, y0, eps и max_iter.
    Пользователь может выбрать ввод из файла или через консоль.
    Формат ввода в файле (одна строка):
         0.1 0 0 1e-5 100
    где alpha=0.1, x0=0, y0=0, eps=1e-5, max_iter=100.
    """
    mode = input("Введите 'file' для чтения параметров из файла или 'console' для ввода с консоли: ").strip().lower()
    if mode == 'file':
        filename = input("Введите название файла с параметрами: ").strip()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
            parts = line.split()
            if len(parts) < 5:
                raise ValueError("В файле должно быть как минимум 5 значений: alpha, x0, y0, eps, max_iter.")
            alpha = float(parts[0])
            x0 = float(parts[1])
            y0 = float(parts[2])
            eps = float(parts[3])
            max_iter = int(parts[4])
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            raise
    else:
        try:
            alpha = float(input("Введите alpha (параметр релаксации): "))
            x0 = float(input("Начальное приближение x0: "))
            y0 = float(input("Начальное приближение y0: "))
            eps = float(input("Точность (eps): "))
            max_iter = int(input("Максимальное число итераций: "))
        except Exception as e:
            print(f"Ошибка ввода: {e}")
            raise

    return alpha, x0, y0, eps, max_iter


def parse_equation(eq_str):
    """
    Преобразует строку уравнения в удобный для sympy вид.
    Заменяет '^' на '**' и удаляет '= 0', если оно присутствует.
    """
    eq_str = eq_str.replace('^', '**')
    eq_str = eq_str.replace('= 0', '')
    return eq_str.strip()


def parse_system(system):
    """
    Принимает список уравнений вида:
        ["x^2 + y^2 - 1 = 0", "x^3 - y = 0"]
    и возвращает символьные выражения expr1, expr2 и символьные переменные x, y.
    """
    if len(system) < 2:
        raise ValueError("Система должна содержать минимум 2 уравнения.")

    eq1 = parse_equation(system[0])
    eq2 = parse_equation(system[1])

    x, y = sympy.symbols('x y', real=True)
    try:
        expr1 = sympy.sympify(eq1)
        expr2 = sympy.sympify(eq2)
    except sympy.SympifyError as e:
        raise ValueError("Ошибка: не удалось преобразовать уравнения в символьные выражения.") from e

    return expr1, expr2, x, y


def iteration_method(system):
    """
    Решает систему нелинейных уравнений методом простых итераций с адаптивным подбором шага.
    Итерационная схема первоначально задаётся как:
         x_{n+1} = x_n - alpha * f1(x_n, y_n)
         y_{n+1} = y_n - alpha * f2(x_n, y_n)
    Если предложенный шаг не уменьшает норму F(x,y) = sqrt(f1^2+f2^2), alpha уменьшается (line search).

    Останавливаемся, если:
      - ||F(x,y)|| < eps,
      - Или изменение (x,y) меньше eps,
      - Или достигнуто число итераций max_iter.
    """
    print(f"[Метод простых итераций] Решаем систему уравнений: {system}")

    # Считываем параметры
    try:
        alpha, x0, y0, eps, max_iter = read_parameters()
    except Exception:
        return

    # Парсим уравнения системы
    try:
        expr1, expr2, x, y = parse_system(system)
    except Exception as e:
        print(e)
        return

    # Преобразуем символьные выражения в функции f1(x,y) и f2(x,y)
    f1 = sympy.lambdify((x, y), expr1, 'math')
    f2 = sympy.lambdify((x, y), expr2, 'math')

    current_x, current_y = x0, y0
    iter_count = 0

    for i in range(max_iter):
        try:
            f_val1 = f1(current_x, current_y)
            f_val2 = f2(current_x, current_y)
        except Exception as e:
            print(f"Ошибка при вычислении функции в точке ({current_x}, {current_y}): {e}")
            return

        norm_f = math.sqrt(f_val1 ** 2 + f_val2 ** 2)
        if norm_f < eps:
            print(f"Сходимость по значению функции достигнута: ||F(x,y)|| = {norm_f} < {eps}")
            break

        # Адаптивный подбор шага
        alpha_current = alpha
        candidate_found = False
        max_backtracks = 20  # максимальное число попыток уменьшить шаг
        for j in range(max_backtracks):
            candidate_x = current_x - alpha_current * f_val1
            candidate_y = current_y - alpha_current * f_val2
            try:
                candidate_f1 = f1(candidate_x, candidate_y)
                candidate_f2 = f2(candidate_x, candidate_y)
            except Exception as e:
                print(f"Ошибка при вычислении функции в кандидате ({candidate_x}, {candidate_y}): {e}")
                break

            norm_candidate = math.sqrt(candidate_f1 ** 2 + candidate_f2 ** 2)
            if norm_candidate < norm_f:
                candidate_found = True
                break
            # Уменьшаем шаг, если улучшения нет
            alpha_current /= 2

        if not candidate_found:
            print("Не удалось найти улучшение на данной итерации. Возможно, метод не сходится с выбранным alpha.")
            break

        diff = math.sqrt((candidate_x - current_x) ** 2 + (candidate_y - current_y) ** 2)
        current_x, current_y = candidate_x, candidate_y
        iter_count = i + 1

        # Если изменение решения меньше eps, считаем, что сходимость достигнута
        if diff < eps:
            print(f"Сходимость по изменению решения достигнута: ||Δ(x,y)|| = {diff} < {eps}")
            break

        # Проверка на возможную расходимость
        if abs(current_x) > 1e15 or abs(current_y) > 1e15:
            print(f"Итерации расходятся: x = {current_x}, y = {current_y}. Прерывание вычислений.")
            return

    else:
        print("Достигнуто максимальное число итераций.")

    # Итоговая оценка
    try:
        final_f1 = f1(current_x, current_y)
        final_f2 = f2(current_x, current_y)
    except Exception as e:
        print(f"Ошибка при финальном вычислении функций: {e}")
        return

    print("\nРезультаты решения системы методом простых итераций с адаптивным шагом:")
    print(f"Найденное решение: x = {current_x}, y = {current_y}")
    print(f"Число итераций: {iter_count}")
    print(f"||F(x,y)|| = {math.sqrt(final_f1 ** 2 + final_f2 ** 2)}")


if __name__ == '__main__':
    # Пример ввода уравнений:
    # Например, x^2 + y^2 - 1 = 0 и x^3 - y = 0
    system_input = []
    n = 2  # число уравнений в системе
    for i in range(n):
        eq = input(f"Введите уравнение {i + 1} (например, x^2 + y^2 - 1 = 0): ")
        system_input.append(eq)
    iteration_method(system_input)
