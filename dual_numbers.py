import math


class Dual_number:
    def __init__(self, re=0., im=0.):
        self.re = re
        self.im = im

    # Перевод в int при self.im = 0
    def __int__(self):
        if self.im == 0:
            return int(self.re)
        raise ValueError("Нельзя преобразовать в int")

    # Перевод в float при self.im = 0
    def __float__(self):
        if self.im == 0:
            return float(self.re)
        raise ValueError("Нельзя преобразовать в float")

    # Сопряженное число
    def conj(self):
        return Dual_number(self.re, -self.im)

    # Аналог угла числа
    def ang(self):
        return self.im / self.re

    # Модуль числа
    def __abs__(self):
        return self.re

    # Вывод числа
    def __str__(self):
        return f'{self.re}{self.im:+}ε'

    def __pos__(self):
        return Dual_number(self)

    def __neg__(self):
        return Dual_number(-self.re, -self.im)

    # Сложение чисел
    def __add__(self, other):
        if isinstance(other, Dual_number):
            return Dual_number(self.re + other.re, self.im + other.im)
        elif isinstance(other, int) or isinstance(other, float):
            return Dual_number(self.re + other, self.im)
        raise TypeError("Неправильный тип переменной")

    __radd__ = __add__
    __iadd__ = __add__

    # Вычитание чисел
    def __sub__(self, other):
        if isinstance(other, Dual_number):
            return Dual_number(self.re - other.re, self.im - other.im)
        elif isinstance(other, int) or isinstance(other, float):
            return Dual_number(self.re - other, self.im)
        raise TypeError("Неправильный тип переменной")

    def __rsub__(self, other):
        if isinstance(other, Dual_number):
            return Dual_number(self.re - other.re, self.im - other.im)
        elif isinstance(other, int) or isinstance(other, float):
            return Dual_number(other - self.re, -self.im)
        raise TypeError("Неправильный тип переменной")

    __isub__ = __sub__

    # Умножение чисел
    def __mul__(self, other):
        if isinstance(other, Dual_number):
            return Dual_number(self.re * other.re,
                               self.re * other.im + self.im * other.re)
        elif isinstance(other, int) or isinstance(other, float):
            return Dual_number(self.re * other, self.im * other)
        raise TypeError("Неправильный множитель")

    __rmul__ = __mul__
    __imul__ = __mul__

    # Деление чисел
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Dual_number(self.re / other, self.im / other)
        elif isinstance(other, Dual_number):
            if other.re != 0:
                return Dual_number(self.re / other.re, (self.im * other.re - self.re * other.im) / other.re ** 2)
            elif self.re == 0:
                # Для определенности в этом случае мнимая часть равна 0
                return Dual_number(self.im / other.im, 0)
            else:
                raise ValueError("Нет решения")
        raise TypeError("Неправильный делитель")

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if self.re != 0:
                return Dual_number(other / self.re, -other * self.im / self.re ** 2)
            elif other == 0:
                # Аналогично прошлому пункту, мнимая часть равна 0
                return Dual_number(0, 0)
            else:
                raise ValueError("Нет решения")
        raise TypeError("Неправильное делимое")

    __itruediv__ = __truediv__

    # Возведение в степень
    def __pow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Dual_number(self.re ** other, self.re ** (other - 1) * other * self.im)
        elif isinstance(other, Dual_number):
            return Dual_number(self.re ** other.re,
                               self.re ** other.re * other.im * math.log(self.re) + self.re ** (
                                           other.re - 1) * other.re * self.im)
        raise TypeError("Неправильная степень")

    def __rpow__(self, other):
        if isinstance(other, Dual_number):
            return other ** self
        elif isinstance(other, int) or isinstance(other, float):
            return Dual_number(other ** self.re, other ** self.re * self.im * math.log(other))
        raise TypeError("Неправильное основание показательной функции")

    __ipow__ = __pow__

    # Равенство чисел
    def __eq__(self, other):
        if isinstance(other, Dual_number):
            if self.re == other.re and self.im == other.im:
                return True
            else:
                return False
        elif isinstance(other, int) or isinstance(other, float):
            if self.im == 0 and self.re == other:
                return True
            else:
                return False
        raise TypeError("Невозможно сравнить объекты")

    # Неравенство чисел
    def __ne__(self, other):
        return not (self == other)


eps = Dual_number(0, 1)


def log(x, base=math.e):
    # Возвращает логарифм от x
    if (isinstance(base, int) or isinstance(base, float)) and (isinstance(x, int) or isinstance(x, float)):
        return math.log(x, base)
    elif (isinstance(base, int) or isinstance(base, float)) and isinstance(x, Dual_number):
        return (log(x.re) + x.im / x.re * eps) / log(base)
    elif isinstance(x, Dual_number) and isinstance(base, Dual_number):
        return log(x) / log(base)
    raise TypeError("Неправильные аргументы логарифма")


def exp(x):
    # Возвращает экспоненту от x
    if isinstance(x, int) or isinstance(x, float):
        return math.exp(x)
    elif isinstance(x, Dual_number):
        return math.e ** x
    raise TypeError("Неправильный аргумент экспоненты")


def sin(x):
    # Возвращает синус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.sin(x)
    elif isinstance(x, Dual_number):
        return math.sin(x.re) + x.im * math.cos(x.re) * eps
    raise TypeError("Неправильный аргумент синуса")


def cos(x):
    # Возвращает косинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.cos(x)
    elif isinstance(x, Dual_number):
        return math.cos(x.re) - x.im * math.sin(x.re) * eps
    raise TypeError("Неправильный аргумент косинуса")


def tan(x):
    # Возвращает тангенс от x
    if isinstance(x, int) or isinstance(x, float):
        return math.tan(x)
    elif isinstance(x, Dual_number):
        return math.tan(x.re) + (math.tan(x.re) ** 2 + 1) * x.im * eps
    raise TypeError("Неправильный аргумент тангенса")


def ctn(x):
    # Возвращает котангенс от x
    if isinstance(x, int) or isinstance(x, float):
        return math.tan(math.pi / 2 - x)
    elif isinstance(x, Dual_number):
        return math.tan(math.pi / 2 - x.re) - x.im * eps / math.sin(x.re) ** 2
    raise TypeError("Неправильный аргумент котангенса")


def asin(x):
    # Возвращает арксинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.asin(x)
    elif isinstance(x, Dual_number):
        return math.asin(x.re) + x.im * eps / math.sqrt(1 - x.re ** 2)
    raise TypeError("Неправильный аргумент арксинуса")


def acos(x):
    # Возвращает арккосинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.acos(x)
    elif isinstance(x, Dual_number):
        return math.acos(x.re) - x.im * eps / math.sqrt(1 - x.re ** 2)
    raise TypeError("Неправильный аргумент арккосинуса")


def atan(x):
    # Возвращает арктангенс от x
    if isinstance(x, int) or isinstance(x, float):
        return math.atan(x)
    elif isinstance(x, Dual_number):
        return math.atan(x.re) + x.im * eps / (1 + x.re ** 2)
    raise TypeError("Неправильный аргумент арктангенса")


def actn(x):
    # Возвращает арккотангенс от x
    if isinstance(x, int) or isinstance(x, float):
        return math.pi / 2 - math.atan(x)
    elif isinstance(x, Dual_number):
        return math.pi / 2 - math.atan(x.re) - x.im * eps / (1 + x.re ** 2)
    raise TypeError("Неправильный аргумент арккотангенса")


def sinh(x):
    # Возвращает гиперболический синус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.sinh(x)
    elif isinstance(x, Dual_number):
        return math.sinh(x.re) + math.cosh(x.re) * x.im * eps
    raise TypeError("Неправильный аргумент гиперболического синуса")


def cosh(x):
    # Возвращает гиперболический косинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.cosh(x)
    elif isinstance(x, Dual_number):
        return math.cosh(x.re) + math.sinh(x.re) * x.im * eps
    raise TypeError("Неправильный аргумент гиперболического косинуса")


def tanh(x):
    # Возвращает аргумент гиперболического тангенса от x
    if isinstance(x, int) or isinstance(x, float):
        return math.tanh(x)
    elif isinstance(x, Dual_number):
        return math.tanh(x.re) + x.im * eps / math.cosh(x.re) ** 2
    raise TypeError("Неправильный аргумент гиперболического тангенса")


def ctnh(x):
    # Возвращает аргумент гиперболического котангенса от x
    if isinstance(x, int) or isinstance(x, float) or isinstance(x, Dual_number):
        return 1 / tanh(x)
    raise TypeError("Неправильный аргумент гиперболического котангенса")


def asinh(x):
    # Возвращает гиперболический арксинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.asinh(x)
    elif isinstance(x, Dual_number):
        return math.asinh(x.re) + x.im * eps / math.sqrt(x.re ** 2 + 1)
    raise TypeError("Неправильный аргумент гиперболического арксинуса")


def acosh(x):
    # Возвращает гиперболический арккосинус от x
    if isinstance(x, int) or isinstance(x, float):
        return math.acosh(x)
    elif isinstance(x, Dual_number):
        return math.acosh(x.re) + x.im * eps / math.sqrt(x.re ** 2 - 1)
    raise TypeError("Неправильный аргумент гиперболического арксинуса")


def atanh(x):
    # Возвращает гиперболический арктангенс от x
    if isinstance(x, int) or isinstance(x, float):
        return math.atanh(x)
    elif isinstance(x, Dual_number):
        return math.atanh(x.re) + x.im * eps / (1 - x.re ** 2)
    raise TypeError("Неправильный аргумент гиперболического арктангенса")


def deriv(func, x):
    # Возвращает значение производной функции func в точке x
    if isinstance(x, int) or isinstance(x, float) or isinstance(x, Dual_number) and x.im == 0:
        return func(x + eps).im
    elif isinstance(x, Dual_number):
        return (func(x) - func(x.re)) / (x.im * eps)
    raise TypeError("Неправильный тип аргумента функции")
