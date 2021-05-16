import os
import sys
import threading
import json
from PyQt5 import QtWidgets

import serial

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        with open('config.json', 'rb') as config_file:
            self.config = json.load(config_file)

        self.serial_lock = threading.Semaphore(1)
        self.serial_interface = serial.Serial(**self.config['serial'])
        self.push_time = -1
        self.current_row = 0

        self.title = 'Quiz Master'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 800

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)

        self.btn_reset = QPushButton('Reset')
        self.btn_reset.setEnabled(True)
        self.btn_reset.clicked.connect(self.reset)

        # Create table
        self.tbl_result = QTableWidget()
        self.tbl_result.setRowCount(10)
        self.tbl_result.setColumnCount(2)
        self.tbl_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_result.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tbl_result)
        self.layout.addWidget(self.btn_reset)
        self.setLayout(self.layout) 

        self.reset()

        # Show widget
        self.show()

    @pyqtSlot()
    def tick(self):
        self.serial_lock.acquire(blocking=False)
        if self.serial_interface.inWaiting():
            serial_input = self.serial_interface.readline()
            serial_input = [chr(x) for x in serial_input]
            serial_input = ''.join(serial_input)
            serial_input = serial_input.replace('\n', '')

            player, _, time = serial_input.split(';')
            time = int(time)
            if player in self.config['player']:
                player = self.config['player'][str(player)]
            else:
                player = f'Player {player}'
            self.add_result(player, time)
        self.serial_lock.release()
        self.timer.start(1)

    @pyqtSlot()
    def reset(self):
        self.serial_lock.acquire(blocking=False)
        self.serial_interface.write(b'reset\n')
        self.push_time = -1
        self.current_row = 0
        self.tbl_result.clear()
        self.serial_lock.release()

    def add_result(self, player, time):
        player_item = QTableWidgetItem(player)
        player_item.setTextAlignment(Qt.AlignCenter)

        if self.push_time < 0:
            self.push_time = time
            time_item = QTableWidgetItem('---')
        else:
            diff = (time - self.push_time) / 1000
            time_item = QTableWidgetItem(f'{diff:0.3f}')
        time_item.setTextAlignment(Qt.AlignCenter)

        if self.current_row == 0:
            background = QColor(self.config['style']['first']['background'])
            font = QFont("Arial", **self.config['style']['first']['font'])
            player_item.setBackground(background)
            player_item.setFont(font)
            time_item.setBackground(background)
            time_item.setFont(font)
        elif self.current_row == 1:
            background = QColor(self.config['style']['second']['background'])
            font = QFont("Arial", **self.config['style']['second']['font'])
            player_item.setBackground(background)
            player_item.setFont(font)
            time_item.setBackground(background)
            time_item.setFont(font)
        elif self.current_row == 2:
            background = QColor(self.config['style']['third']['background'])
            font = QFont("Arial", **self.config['style']['third']['font'])
            player_item.setBackground(background)
            player_item.setFont(font)
            time_item.setBackground(background)
            time_item.setFont(font)
        else:
            background = QColor(self.config['style']['other']['background'])
            font = QFont("Arial", **self.config['style']['other']['font'])
            player_item.setBackground(background)
            player_item.setFont(font)
            time_item.setBackground(background)
            time_item.setFont(font)

        self.tbl_result.setItem(self.current_row, 0, player_item)
        self.tbl_result.setItem(self.current_row, 1, time_item)

        self.current_row += 1

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  