import sys
import math
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
          'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
          'U', 'V', 'W', 'X', 'Y', 'Z']


def is_right(argument, i):
    for symbol in argument:
        try:
            assert symbol in VALUES
            assert VALUES.index(symbol) < i
        except AssertionError:
            return False
    return True


def from_any_to_decimal(argument, i):
    temp = 0
    argument_1 = argument[::-1]
    k = 0
    for symbol in argument_1:
        temp += VALUES.index(symbol) * (i ** k)
        k += 1
    return temp


def from_decimal_to_any(argument, j):
    result = ''
    while argument >= j:
        add = argument % j
        result += str(VALUES[add])
        argument //= j
    result += str(VALUES[argument])
    return result[::-1]


def translation(argument, i, j):
    temp = from_any_to_decimal(argument, i)
    return from_decimal_to_any(temp, j)


class MyWidget(QMainWindow):
    def __init__(self):
        self.i = 2
        self.i_1 = 2
        self.i_2 = 2
        self.i_3 = 2
        self.j = 2
        self.j_1 = 2
        self.j_2 = 2
        self.arithmetic_sign = '+'
        self.arithmetic_sign_1 = '!'
        super().__init__()
        uic.loadUi('MainProject.ui', self)
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
            arg = from_any_to_decimal(number, self.i_1)
            arg_2 = from_any_to_decimal(number_2, self.i_2)
            value = '{}{}{}'.format(int(arg), self.arithmetic_sign, int(arg_2))
            if self.arithmetic_sign == '/' and number_2 == 0:
                self.label_14.setText('На ноль делить нельзя!!!')
            else:
                temp = eval(value)
                self.label_14.setText(from_decimal_to_any(temp, self.j_1))
        else:
            self.label_14.setText('ERROR')

    def active_3(self):
        number = str(self.lineEdit_4.text())
        if is_right(number, self.i_3):
            arg = from_any_to_decimal(number, self.i_3)
            if self.arithmetic_sign_1 == '!':
                temp = math.factorial(int(arg))
                self.label_21.setText(from_decimal_to_any(str(temp), self.j_2))
        else:
            self.label_21.setText('ERROR')


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())