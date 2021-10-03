import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget


app = QApplication(sys.argv)
resolution = QDesktopWidget().availableGeometry()
resolution_ratio = resolution.width() / 1280
save_path = ''
granularity_levels = [['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' '],
                      ['№', '@', '#', 'S', '%', 'a', '?', 'c', '*', '=', '+', ':', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'k', 'a', '?', 'c', 'v', '*', '=', '+', ';',
                       ':', '^', '~', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'U', 'k', 'g', 'h', 'a', '?', 'c', 'v', 't',
                       '*', '=', '+', '!', ';', ':', '^', '~', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'U', 'k', '2', 'g', 'h', 'a', '?', 'c', 'v',
                       '1', 't', '*', '=', '>', '<', '+', '/', '!', ';', ':', '^', '~', ',', '.', '`', ' ']]
