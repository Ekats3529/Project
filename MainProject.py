import sys
import math
from fractions import Fraction
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QButtonGroup
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
          'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
          'U', 'V', 'W', 'X', 'Y', 'Z']
SPECIAL_SYMBOLS = ['(', ')', '.', '-']


def is_right(argument, i):
    for symbol in argument:
        try:
            if symbol == '-':
                assert argument.count(symbol) == 1 and argument.startswith(symbol)
            assert (symbol in VALUES and VALUES.index(symbol) < i) or symbol in SPECIAL_SYMBOLS
        except AssertionError:
            return False
    return True


def int_digits_to_any(argument, j):
    result = ''
    argument_1 = abs(int(argument))
    while argument_1 >= j:
        add = argument_1 % j
        result += str(VALUES[add])
        argument_1 //= j
    result += str(argument_1)
    if result == str(argument_1) and j > 10:
        return VALUES[int(result)]
    elif int(argument) < 0:
        return '-{}'.format(result[::-1])
    else:
        return result[::-1]


def fract_part_to_decimal(argument, i):
    temp1 = 0
    for digit in argument:
        temp1 += Fraction(VALUES.index(digit), (i ** (argument.index(digit) + 1)))
    return str(temp1.numerator), str(temp1.denominator)


def int_digits_to_decimal(argument, i):
    temp = 0
    k = 0
    argument_1 = str(argument)
    integer_part = argument_1[::-1]
    for symbol in integer_part:
        temp += VALUES.index(symbol) * (i ** k)
        k += 1
    if '-' in argument_1:
        return str('-{}'.format(temp))
    return str(temp)


def from_period_to_simple(expression, i):
    temp = expression.split('.')
    integer_part = int_digits_to_decimal(temp[0], i)
    fract_part = temp[-1]
    try:
        period = fract_part[(fract_part.index('(') + 1):fract_part.index(')')]
        integer = fract_part[:fract_part.index('(')]
        both_period_and_integer = int_digits_to_decimal(integer + period, i)
        if integer == '':
            integer = '0'
        if period == '':
            period = '0'
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
    if '-' in str(expression):
        return [str(-int(integer_part)), str(-int(name_1)), str(-int(name_2))]
    else:
        return [integer_part, name_1, name_2]


def from_simple_to_period(numerator, denominator):
    if '/' in str(denominator):
        temp = denominator.split('/')
        numerator = temp[-1]
        denominator = temp[0]
    if '/' in str(numerator):
        temp = numerator.split('/')
        numerator = temp[0]
        denominator = temp[-1]
    rest = {}
    ans = ''
    flag = False
    if int(numerator) < 0:
        numerator = abs(int(numerator))
        flag = True
    numerator = int(numerator)
    denominator = int(denominator)
    integer_part = numerator // denominator
    i = 0
    numerator = numerator % denominator
    rest[numerator] = i
    i += 1
    if numerator == 0:
        if flag:
            return '-{}'.format(integer_part)
        return integer_part
    while True:
        if numerator == 0:
            if flag:
                return '-{}.{}'.format(integer_part, ans)
            return '{}.{}'.format(integer_part, ans)
        digit, numerator = divmod(numerator * 10, denominator)
        ans += str(digit)
        if numerator not in rest:
            rest[numerator] = i
            i += 1
        else:
            if flag:
                return '-{}.{}({})'.format(integer_part, ans[:rest[numerator]], ans[rest[numerator]:])
            return '{}.{}({})'.format(integer_part, ans[:rest[numerator]], ans[rest[numerator]:])


def translation(argument, i, j, decimal=False):
    argument = str(argument)
    flag = False
    if '-' in argument:
        flag = True
        argument = argument[1::]
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
    if '-' in arg2:
        arg2 = arg2[1::]
    elif '-' in arg3:
        arg3 = arg3[1::]
    if arg3 == '1':
        arg3 = '0'
    if decimal:
        if arg3 != '0':
            answer = from_simple_to_period((int(arg1) * int(arg3)) + int(arg2), int(arg3))
        else:
            answer = str(int(arg1) + int(arg2))
    else:
        if arg1 != '0' and arg2 != '0' and arg3 != '0':
            answer = '{} {}/{}'.format(arg1, arg2, arg3)
        elif arg3 == '0':
            answer = str(int(arg1) + int(arg2))
        else:
            answer = '{}/{}'.format(arg2, arg3)
    if flag:
        return '-{}'.format(answer)
    return answer


def evaluate_button(arg1, arg2, sign):
    arg1_1 = arg1.split()
    arg2_1 = arg2.split()
    if len(arg1_1) == 2:
        temp = arg1_1[-1].split('/')
        fract_1 = ('{}/{}'.format((int(arg1_1[0]) * temp[-1]) + temp[0], temp[-1]))
    else:
        if '/' in arg1_1[0]:
            fract_1 = Fraction(arg1_1[0])
        else:
            fract_1 = Fraction('{}/1'.format(arg1_1[0]))
    if len(arg2_1) == 2:
        temp = arg2_1[-1].split('/')
        fract_2 = Fraction('{}/{}'.format((int(arg2_1[0]) * temp[-1]) + temp[0], temp[-1]))
    else:
        if '/' in arg2_1[0]:
            fract_2 = Fraction(arg2_1[0])
        else:
            fract_2 = Fraction('{}/1'.format(arg2_1[0]))
    if sign == '+':
        return fract_1 + fract_2
    elif sign == '-':
        return fract_1 - fract_2
    elif sign == '*':
        return fract_1 * fract_2
    elif sign == '/':
        return fract_1 / fract_2
    elif sign == '%':
        return fract_1 % fract_2
    elif sign == '**':
        return fract_1 ** fract_2
    elif sign == '//':
        return fract_1 // fract_2


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
        self.ch_1 = False
        self.ch_2 = False
        self.ch_3 = False
        self.fr_1 = True
        self.fr_2 = True
        self.fr_3 = True
        self.flag = False
        self.arithmetic_sign = '+'
        self.arithmetic_sign_1 = '!'
        self.setWindowTitle('Калькулятор разных систем счисления')
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
        self.button_group = QButtonGroup()
        self.button_group_2 = QButtonGroup()
        self.button_group_3 = QButtonGroup()
        self.button_group.addButton(self.radioButton)
        self.button_group.addButton(self.radioButton_2)
        self.radioButton_2.setChecked(True)
        self.button_group_2.addButton(self.radioButton_3)
        self.button_group_2.addButton(self.radioButton_4)
        self.radioButton_4.setChecked(True)
        self.button_group_3.addButton(self.radioButton_5)
        self.button_group_3.addButton(self.radioButton_6)
        self.radioButton_6.setChecked(True)
        self.button_group.buttonClicked.connect(self.choice_1)
        self.button_group_2.buttonClicked.connect(self.choice_2)
        self.button_group_3.buttonClicked.connect(self.choice_3)

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
        if number != '':
            if is_right(number, self.i):
                if not self.ch_1 and self.fr_1:
                    self.label_6.setText(translation(number, self.i, self.j))
                elif ((self.ch_1 and not self.fr_1) or (not self.ch_1 and not self.fr_1)) and int(self.j) == 10:
                    self.label_6.setText(translation(number, self.i, self.j, True))
                elif (not self.ch_1 and not self.fr_1) or int(self.j) != 10:
                    self.label_6.setText('ERROR')
            else:
                self.label_6.setText('ERROR')
        else:
            self.label_6.setText('Введите число')

    def active_2(self):
        number = str(self.lineEdit_2.text())
        number_2 = str(self.lineEdit_3.text())
        if number != '' and number_2 != '':
            if is_right(number, self.i_1) and is_right(number_2, self.i_2):
                arg = translation(number, self.i_1, 10)
                arg_2 = translation(number_2, self.i_2, 10)
                if self.arithmetic_sign == '/' and number_2 == '0':
                    self.label_14.setText('Деление на ноль невозможно')
                else:
                    print(3)
                    temp = evaluate_button(arg, arg_2, self.arithmetic_sign)
                    print(4)
                    temp1 = from_simple_to_period(temp.numerator, temp.denominator)
                    print(5)
                    if ((self.ch_2 and not self.fr_2) or (not self.ch_2 and not self.fr_2)) and int(self.j_1) == 10:
                        print(6)
                        self.label_14.setText(translation(temp1, 10, self.j_1, True))

                    elif not self.ch_2 and self.fr_2:
                        print(7)
                        self.label_14.setText(translation(temp1, 10, self.j_1))
                    elif (not self.ch_2 and not self.fr_2) or int(self.j_1) != 10:
                        print(8)
                        self.label_14.setText('ERROR')
            else:
                self.label_14.setText('ERROR')
        else:
            self.label_14.setText('Введите число')

    def active_3(self):
        number = str(self.lineEdit_4.text())
        if number != '':
            if is_right(number, self.i_3):
                if '.' not in number and '-' not in number:
                    flag = True
                else:
                    flag = False
                if '-' not in number:
                    flag_2 = True
                else:
                    flag_2 = False
                if flag:
                    arg = int_digits_to_decimal(number, self.i_3)
                else:
                    arg = translation(number, self.i_3, 10)
                if self.arithmetic_sign_1 == '!' and flag:
                    temp = math.factorial(int(arg))
                    self.label_21.setText(str(int_digits_to_any(str(temp), self.j_2)))
                elif self.arithmetic_sign_1 == '^(-1)':
                    temp = from_simple_to_period(1, arg)
                    if ((self.ch_3 and not self.fr_3) or (not self.ch_3 and not self.fr_3)) and int(self.j_2) == 10:
                        temp = translation(temp, 10, self.j_2, True)
                    elif not self.ch_3 and self.fr_3:
                        temp = translation(temp, 10, self.j_2)
                    elif (not self.ch_3 and not self.fr_3) or int(self.j_2) != 10:
                        temp = 'ERROR'
                    self.label_21.setText(temp)
                elif flag_2 and self.arithmetic_sign_1 != '!' and self.arithmetic_sign_1 != '^(-1)':
                    try:
                        temp = math.sqrt(float(from_simple_to_period(arg, 1)))
                        self.flag = False
                    except Exception:
                        self.ch_3 = False
                        self.fr_3 = False
                        self.flag = True
                    if ((self.ch_3 and not self.fr_3) or (not self.ch_3 and not self.fr_3)) and int(self.j_2) == 10:
                        if not self.flag:
                            temp = translation(temp, 10, self.j_2, True)
                        else:
                            temp = 'ERROR'
                    elif not self.ch_3 and self.fr_3:
                        temp = translation(temp, 10, self.j_2)
                    elif ((not self.ch_3 and not self.fr_3) or int(self.j_2) != 10) and self.flag:
                        temp = 'ERROR'
                    self.label_21.setText(temp)
                else:
                    self.label_21.setText('ERROR')
            else:
                self.label_21.setText('ERROR')
        else:
            self.label_21.setText('Введите число')

    def choice_1(self, button):
        if button.text() == 'В виде десятичной дроби':
            if int(self.j) == 10:
                self.ch_1 = True
                self.fr_1 = False
            else:
                self.ch_1 = False
                self.fr_1 = False
        else:
            self.ch_1 = False
            self.fr_1 = True

    def choice_2(self, button):
        if button.text() == 'В виде десятичной дроби':
            if int(self.j_1) == 10:
                self.ch_2 = True
                self.fr_2 = False
            else:
                self.ch_2 = False
                self.fr_2 = False
        else:
            self.ch_2 = False
            self.fr_2 = True

    def choice_3(self, button):
        if button.text() == 'В виде десятичной дроби':
            if int(self.j_2) == 10:
                self.ch_3 = True
                self.fr_3 = False
            else:
                self.ch_3 = False
                self.fr_3 = False
        else:
            self.ch_3 = False
            self.fr_3 = True


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())

