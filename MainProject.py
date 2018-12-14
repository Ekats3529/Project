import sys
import math
from fractions import Fraction
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
          'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
          'U', 'V', 'W', 'X', 'Y', 'Z']
SPECIAL_SYMBOLS = ['(', ')', '.']


def is_right(argument, i):
    for symbol in argument:
        try:
            assert (symbol in VALUES and VALUES.index(symbol) < i) or symbol in SPECIAL_SYMBOLS
        except AssertionError:
            return False
    return True


def int_digits_to_any(argument, j):
    result = ''
    argument = int(argument)
    while argument >= j:
        add = argument % j
        result += str(VALUES[add])
        argument //= j
    result += str(argument)
    if result == str(argument) and j > 10:
        return VALUES[int(result)]
    return result[::-1]


def fract_part_to_decimal(argument, i):
    temp1 = 0
    for digit in argument:
        temp1 += Fraction(VALUES.index(digit), (i ** (argument.index(digit) + 1)))
    return str(temp1.numerator), str(temp1.denominator)


def int_digits_to_decimal(argument, i):
    temp = 0
    k = 0
    integer_part = argument[::-1]
    for symbol in integer_part:
        temp += VALUES.index(symbol) * (i ** k)
        k += 1
    return str(temp)


def from_period_to_simple(expression, i):
    temp = expression.split('.')
    integer_part = int_digits_to_decimal(temp[0], i)
    fract_part = temp[-1]
    try:
        period = fract_part[(fract_part.index('(') + 1):fract_part.index(')')]
        integer = fract_part[:fract_part.index('(')]
        both_period_and_integer = int_digits_to_decimal(integer + period, i)
        numerator = int(both_period_and_integer) - int(int_digits_to_decimal(integer, i))
        if period == '0':
            period = ''
        if integer == '0':
            integer = ''
        denominator = int(int_digits_to_decimal(str(len(period) * str(i - 1)) + str(len(integer) * '0'), i))
        f = Fraction(numerator, denominator)
    except ValueError:
        temp = fract_part_to_decimal(fract_part, i)
        f = Fraction('{}/{}'.format(int(temp[0]), temp[-1]))
    name_1 = f.numerator
    name_2 = f.denominator
    return [integer_part, name_1, name_2]


def from_simple_to_period(numerator, denominator):
    rest = {}
    ans = ''
    numerator = int(numerator)
    denominator = int(denominator)
    integer_part = numerator // denominator
    i = 0
    numerator = numerator % denominator
    rest[numerator] = i
    i += 1
    if numerator == 0:
        return integer_part
    while True:
        if numerator == 0:
            return '{}.{}'.format(integer_part, ans)
        digit, numerator = divmod(numerator * 10, denominator)
        ans += str(digit)
        if numerator not in rest:
            rest[numerator] = i
            i += 1
        else:
            return '{}.{}({})'.format(integer_part, ans[:rest[numerator]], ans[rest[numerator]:])


def translation(argument, i, j):
    argument = str(argument)
    integer_part = '0'
    numerator = '0'
    denominator = '0'
    if '(' in argument or '.' in argument:
        temp = from_period_to_simple(argument, i)
        integer_part = temp[0]
        numerator = temp[1]
        denominator = temp[-1]
    elif '.' not in argument and '(' not in argument:
        integer_part = int_digits_to_decimal(argument, i)
        numerator = '0'
        denominator = '0'
    arg1 = str(int_digits_to_any(integer_part, j))
    arg2 = str(int_digits_to_any(numerator, j))
    arg3 = str(int_digits_to_any(denominator, j))
    if arg1 != '0' and arg2 != '0' and arg3 != '0':
        return '{} {}/{}'.format(arg1, arg2, arg3)
    elif arg2 == '0' and arg3 == '0':
        return arg1
    else:
        return '{}/{}'.format(arg2, arg3)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainProject.ui', self)
        self.i = 2
        self.i_1 = 2
        self.i_2 = 2
        self.i_3 = 2
        self.j = 2
        self.j_1 = 2
        self.j_2 = 2
        self.arithmetic_sign = '+'
        self.arithmetic_sign_1 = '!'
        self.pushButton.clicked.connect(self.active_1)
        self.pushButton_2.clicked.connect(self.active_2)
        self.pushButton_3.clicked.connect(self.active_3)
        self.comboBox.activated[str].connect(self.system_1)
        self.comboBox_2.activated[str].connect(self.system_2)
        self.comboBox_3.activated[str].connect(self.system_3)
        self.comboBox_4.activated[str].connect(self.system_4)
        self.comboBox_5.activated[str].connect(self.sign)
        self.comboBox_6.activated[str].connect(self.system_5)
        self.comboBox_7.activated[str].connect(self.system_6)
        self.comboBox_8.activated[str].connect(self.sign_1)
        self.comboBox_9.activated[str].connect(self.system_7)

    def system_1(self, text):
        self.i = int(text)

    def system_2(self, text):
        self.j = int(text)

    def system_3(self, text):
        self.i_1 = int(text)

    def system_4(self, text):
        self.i_2 = int(text)

    def system_5(self, text):
        self.j_1 = int(text)

    def system_6(self, text):
        self.i_3 = int(text)

    def system_7(self, text):
        self.j_2 = int(text)

    def sign(self, text):
        self.arithmetic_sign = text

    def sign_1(self, text):
        self.arithmetic_sign_1 = text

    def active_1(self):
        number = str(self.lineEdit.text())
        if is_right(number, self.i):
            self.label_6.setText(translation(number, self.i, self.j))
        else:
            self.label_6.setText('ERROR')

    def active_2(self):
        number = str(self.lineEdit_2.text())
        number_2 = str(self.lineEdit_3.text())
        if is_right(number, self.i_1) and is_right(number_2, self.i_2):
            arg = int_digits_to_decimal(number, self.i_1)
            arg_2 = int_digits_to_decimal(number_2, self.i_2)
            value = '{}{}{}'.format(int(arg), self.arithmetic_sign, int(arg_2))
            if self.arithmetic_sign == '/' and number_2 == '0':
                self.label_14.setText('На ноль делить нельзя!!!')
            elif self.arithmetic_sign == '/':
                temp = from_simple_to_period(arg, arg_2)
                temp = translation(temp, 10, self.j_1)
                self.label_14.setText(temp)
            else:
                temp = eval(value)
                self.label_14.setText(int_digits_to_any(temp, self.j_1))
        else:
            self.label_14.setText('ERROR')

    def active_3(self):
        number = str(self.lineEdit_4.text())
        if is_right(number, self.i_3):
            arg = int_digits_to_decimal(number, self.i_3)
            if self.arithmetic_sign_1 == '!':
                temp = math.factorial(int(arg))
                self.label_21.setText(str(int_digits_to_any(str(temp), self.j_2)))
            elif self.arithmetic_sign_1 == '^(-1)':
                temp = from_simple_to_period(1, arg)
                temp = translation(temp, 10, self.j_2)
                self.label_21.setText(temp)
            else:
                temp = math.sqrt(int(arg))
                temp = translation(temp, 10, self.j_2)
                self.label_21.setText(temp)
        else:
            self.label_21.setText('ERROR')


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
