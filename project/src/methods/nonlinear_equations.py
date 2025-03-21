import sympy
import math

def chord_method(equation):
    """
    Метод хорд для решения нелинейного уравнения equation (например, 'x^2 - 5 = 0').

    Шаги:
      1) Спросить у пользователя: 'Ввод из файла или с консоли?'
      2) Получить параметры (a, b, eps, max_iter).
      3) Проверить наличие более одного корня на отрезке [a, b] (эвристика).
      4) Применить метод хорд и вывести результат.
    """

    print(f"[Метод хорд] Решаем уравнение: {equation}")

    # --- Шаг 1. Спросим у пользователя про метод ввода параметров
    mode = input("Введите 'file' для чтения из файла или 'console' для ввода с консоли: ").strip().lower()

    # --- Шаг 2. Считываем параметры
    if mode == 'file':
        filename = input("Введите название файла с параметрами: ").strip()
        # Предположим, в файле одна строка вида: 1 2 1e-5 100
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
                parts = line.split()
                if len(parts) < 4:
                    print("Ошибка: в файле должно быть минимум 4 числа (a, b, eps, max_iter).")
                    return
                a, b, eps, max_iter = parts
                a = float(a)
                b = float(b)
                eps = float(eps)
                max_iter = int(max_iter)

        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return
        except ValueError:
            print("Ошибка: некорректный формат данных в файле.")
            return

    else:
        # Ввод с консоли
        try:
            a = float(input("Левая граница (a): "))
            b = float(input("Правая граница (b): "))
            eps = float(input("Точность (eps): "))
            max_iter = int(input("Максимальное число итераций: "))
        except ValueError:
            print("Ошибка: введены некорректные значения.")
            return

    # --- Шаг 3. Подготовка символьного представления уравнения и функции f(x)

    # Убираем из уравнения '= 0', если оно есть, чтобы осталось только выражение
    eq_str = equation.replace('= 0', '').strip()

    # Создаём символ x и преобразуем строку в символьное выражение
    x = sympy.Symbol('x', real=True)
    try:
        expr = sympy.sympify(eq_str)  # Преобразуем строку в выражение Sympy
    except sympy.SympifyError:
        print("Ошибка: не удалось разобрать уравнение.")
        return

    # Создаём функцию f(x) через lambdify (быстрее, чем expr.subs)
    f = sympy.lambdify(x, expr, 'numpy')  # Используем модуль math или numpy

    # --- Шаг 4. Эвристическая проверка на количество корней
    #     (если в [a, b] более одного корня, то метод может найти не тот или не сойтись)
    sign_changes_count = 0
    samples = 100  # кол-во равномерных точек для проверки
    step = (b - a) / samples
    prev_sign = math.copysign(1, f(a)) if f(a) != 0 else 0

    for i in range(1, samples+1):
        xi = a + i * step
        val = f(xi)
        curr_sign = math.copysign(1, val) if val != 0 else 0
        if curr_sign != prev_sign and curr_sign != 0 and prev_sign != 0:
            sign_changes_count += 1
        prev_sign = curr_sign

    if sign_changes_count > 1:
        print("Внимание! Похоже, что в заданном интервале [a, b] может быть более одного корня.")

    # Дополнительно классическая проверка: f(a)*f(b)
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        print("Предупреждение: f(a)*f(b) > 0 — нет гарантии, что на [a,b] ровно один корень.")
        # Можно здесь спросить: "Хотите продолжить?" и т.д.

    # --- Шаг 5. Итерации метода хорд
    # Фиксируем "якорь" в точке a, начинаем итерации с x0 = b
    x_cur = b
    iter_count = 0

    # Чтобы избежать деления на 0, проверяем, что f(a) != f(x_cur)
    if abs(fa - fb) < 1e-15:
        print("Ошибка: f(a) и f(b) слишком близки. Метод хорд может дать деление на 0.")
        return

    for i in range(max_iter):
        # x_{n+1} = x_n - f(x_n)*(x_n - a)/(f(x_n) - f(a))
        fx_cur = f(x_cur)
        denom = (fx_cur - fa)
        if abs(denom) < 1e-15:
            print("Деление на 0 или близко к тому, метод хорд не применим.")
            return

        x_next = x_cur - fx_cur*(x_cur - a)/denom

        if abs(x_next - x_cur) < eps:
            # Считаем, что достигли нужной точности
            root = x_next
            iter_count = i + 1
            break

        x_cur = x_next
        iter_count = i + 1

    else:
        # Если цикл for завершился без break, берём текущее x_cur
        root = x_cur

    # --- Шаг 6. Выводим результат
    print(f"\nНайденный корень: {root}")
    print(f"Количество итераций: {iter_count}")
    print(f"Значение f(root): {f(root)}")

def newton_method(equation: str):
    """
    Метод Ньютона для нахождения корня нелинейного уравнения.

    Параметры:
        equation (str): Строка с уравнением, например "x^2 - 5 = 0".

    Внутри функции запрашивается у пользователя:
        - начальное приближение x0,
        - точность eps,
        - максимальное количество итераций max_iter.

    Пользователь выбирает способ ввода параметров: из файла или с консоли.
    """

    print(f"[Метод Ньютона] Решаем уравнение: {equation}")

    # --- Шаг 1. Спросим у пользователя про метод ввода параметров
    mode = input("Введите 'file' для чтения из файла или 'console' для ввода с консоли: ").strip().lower()

    # --- Шаг 2. Считываем параметры
    if mode == 'file':
        filename = input("Введите название файла с параметрами: ").strip()
        # Предположим, в файле одна строка вида: 1.0 1e-5 100
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
                parts = line.split()
                if len(parts) < 3:
                    print("Ошибка: в файле должно быть минимум 3 числа (x0, eps, max_iter).")
                    return None
                x0 = float(parts[0])
                tol = float(parts[1])
                max_iter = int(parts[2])
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return None
        except ValueError:
            print("Ошибка: некорректный формат данных в файле.")
            return None

    elif mode == 'console':
        try:
            x0 = float(input("Введите начальное приближение (x0): "))
            tol = float(input("Введите точность (eps): "))
            max_iter = int(input("Введите максимальное количество итераций: "))
        except ValueError:
            print("Ошибка: введены некорректные значения.")
            return None
    else:
        print("Неверный режим ввода параметров.")
        return None

    # --- Подготовка символьного выражения
    eq = equation.replace("^", "**")
    if "=" in eq:
        left, right = eq.split("=")
        eq = f"({left}) - ({right})"

    x = sympy.symbols('x')

    allowed_locals = {
        "sin": sympy.sin, "cos": sympy.cos, "tan": sympy.tan,
        "exp": sympy.exp, "E": sympy.E, "sqrt": sympy.sqrt, "pi": sympy.pi
    }

    try:
        f = sympy.sympify(eq, locals=allowed_locals)
    except Exception as e:
        print("Ошибка при разборе уравнения:", e)
        return None

    fprime = sympy.diff(f, x)

    xn = x0
    for i in range(max_iter):
        f_val = f.subs(x, xn)
        fprime_val = fprime.subs(x, xn)

        if fprime_val == 0:
            print("Нулевая производная. Метод Ньютона не применим.")
            return None

        xn_next = xn - f_val / fprime_val

        if abs(xn_next - xn) < tol:
            print(f"Найденный корень: {float(xn_next)} за {i + 1} итераций.")
            return float(xn_next), i + 1

        xn = xn_next

    print(f"Приближённый корень после {max_iter} итераций: {float(xn)}.")
    return float(xn), max_iter


import sympy


def read_parameters():
    """
    Считывает параметры метода: alpha, x0, eps и max_iter.
    Пользователь может выбрать ввод из файла или через консоль.
    Возвращает: (alpha, x0, eps, max_iter)
    """
    mode = input("Введите 'file' для чтения из файла или 'console' для ввода с консоли: ").strip().lower()
    if mode == 'file':
        filename = input("Введите название файла с параметрами: ").strip()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
                parts = line.split()
                if len(parts) < 4:
                    raise ValueError("В файле должно быть 4 числа: alpha, x0, eps, max_iter.")
                alpha = float(parts[0])
                x0 = float(parts[1])
                eps = float(parts[2])
                max_iter = int(parts[3])
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            raise
        except ValueError as e:
            print("Ошибка: некорректные данные в файле.", e)
            raise
    else:
        try:
            alpha = float(input("Введите alpha (параметр релаксации): "))
            x0 = float(input("Начальное приближение (x0): "))
            eps = float(input("Точность (eps): "))
            max_iter = int(input("Максимальное число итераций: "))
        except ValueError as e:
            print("Ошибка: введены некорректные значения.", e)
            raise

    return alpha, x0, eps, max_iter


def parse_equation(equation_str):
    """
    Преобразует строку с уравнением в символьное выражение f(x)=0.
    Поддерживает запись уравнения с символом '^' для возведения в степень.
    Пример: "x^2 + 2 = 10" преобразуется в "(x**2 + 2) - (10)".
    """
    # Убираем лишние пробелы и заменяем '^' на '**'
    eq_str = equation_str.strip().replace('^', '**')

    # Если есть знак "=", приводим к виду f(x)=0
    if '=' in eq_str:
        left, right = eq_str.split('=', 1)
        eq_str = f"({left}) - ({right})"

    # Убираем возможное "= 0"
    eq_str = eq_str.replace('= 0', '').strip()

    x = sympy.symbols('x')
    try:
        expr = sympy.sympify(eq_str)
    except sympy.SympifyError as e:
        print("Ошибка: не удалось преобразовать уравнение в символьное выражение.", e)
        raise

    return expr


def iteration_method(equation):
    """
    Решает уравнение f(x)=0 методом простых итераций.
    Итерационная формула: x_{n+1} = x_n - alpha * f(x_n)

    Остановка производится, если:
      - |f(x_n)| < eps,
      - |x_{n+1} - x_n| < eps,
      - достигнуто число итераций max_iter.

    На вход подаётся строка уравнения, например: "x^2 + 2 = 10".
    """
    print(f"[Метод простых итераций] Решаем уравнение: {equation}")

    # Считываем параметры
    try:
        alpha, x0, eps, max_iter = read_parameters()
    except Exception:
        return

    # Преобразуем уравнение в символьное выражение
    try:
        expr = parse_equation(equation)
    except Exception:
        return

    # Получаем функцию f(x)
    x = sympy.symbols('x')
    f = sympy.lambdify(x, expr, 'math')

    iter_count = 0
    current_x = x0

    for i in range(max_iter):
        fx_val = f(current_x)

        # Проверка условия по значению функции
        if abs(fx_val) < eps:
            print(f"Условие |f(x)| < eps выполнено: |{fx_val}| < {eps}")
            break

        next_x = current_x - alpha * fx_val

        # Проверка условия по изменению x
        if abs(next_x - current_x) < eps:
            current_x = next_x
            iter_count = i + 1
            print(f"Разница между итерациями меньше eps: |{next_x - current_x}| < {eps}")
            break

        # Проверка на возможное расхождение
        if abs(next_x) > 1e15:
            print(f"Итерации расходятся (x ~ {next_x}). Прерываем вычисления.")
            return

        current_x = next_x
        iter_count = i + 1

    final_fx = f(current_x)
    print(f"\nНайденный корень: {current_x}")
    print(f"Количество итераций: {iter_count}")
    if abs(final_fx) < eps:
        print("Условие |f(x)| < eps выполнено.")