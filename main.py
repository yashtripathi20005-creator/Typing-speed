"""
Typing Speed Test Application
Main entry point for the application
"""

import sys
from typing_speed_test import TypingSpeedTest
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = TypingSpeedTest()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
