"""
Results Dialog - Displays typing test results
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette


class ResultsDialog(QDialog):
    """Dialog showing typing test results"""
    
    def __init__(self, wpm, accuracy, total_chars, correct_chars, incorrect_chars, words_typed, total_words):
        super().__init__()
        self.wpm = wpm
        self.accuracy = accuracy
        self.total_chars = total_chars
        self.correct_chars = correct_chars
        self.incorrect_chars = incorrect_chars
        self.words_typed = words_typed
        self.total_words = total_words
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the results dialog UI"""
        self.setWindowTitle("📊 Typing Test Results")
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 44, 52))
        self.setPalette(palette)
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title
        title_label = QLabel("📊 Test Results")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #61afef; margin: 20px;")
        main_layout.addWidget(title_label)
        
        # Stats grid
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #1e222a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        stats_layout = QGridLayout()
        stats_frame.setLayout(stats_layout)
        
        # WPM
        wpm_label = QLabel("⚡ Speed")
        wpm_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        wpm_value = QLabel(f"{self.wpm} WPM")
        wpm_value.setFont(QFont("Arial", 20, QFont.Bold))
        wpm_value.setStyleSheet("color: #61afef;")
        stats_layout.addWidget(wpm_label, 0, 0)
        stats_layout.addWidget(wpm_value, 1, 0)
        
        # Accuracy
        acc_label = QLabel("🎯 Accuracy")
        acc_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        acc_value = QLabel(f"{self.accuracy:.1f}%")
        acc_value.setFont(QFont("Arial", 20, QFont.Bold))
        
        # Color based on accuracy
        if self.accuracy >= 90:
            acc_value.setStyleSheet("color: #98c379;")
        elif self.accuracy >= 70:
            acc_value.setStyleSheet("color: #e5c07b;")
        else:
            acc_value.setStyleSheet("color: #e06c75;")
        
        stats_layout.addWidget(acc_label, 0, 1)
        stats_layout.addWidget(acc_value, 1, 1)
        
        # Characters
        char_label = QLabel("📝 Characters")
        char_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        char_value = QLabel(f"{self.correct_chars}/{self.total_chars}")
        char_value.setFont(QFont("Arial", 16, QFont.Bold))
        char_value.setStyleSheet("color: #c678dd;")
        stats_layout.addWidget(char_label, 0, 2)
        stats_layout.addWidget(char_value, 1, 2)
        
        # Progress
        progress_label = QLabel("📖 Progress")
        progress_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        progress_value = QLabel(f"{self.words_typed}/{self.total_words}")
        progress_value.setFont(QFont("Arial", 16, QFont.Bold))
        progress_value.setStyleSheet("color: #e5c07b;")
        stats_layout.addWidget(progress_label, 2, 0)
        stats_layout.addWidget(progress_value, 3, 0)
        
        # Correct
        correct_label = QLabel("✅ Correct")
        correct_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        correct_value = QLabel(str(self.correct_chars))
        correct_value.setFont(QFont("Arial", 16, QFont.Bold))
        correct_value.setStyleSheet("color: #98c379;")
        stats_layout.addWidget(correct_label, 2, 1)
        stats_layout.addWidget(correct_value, 3, 1)
        
        # Incorrect
        incorrect_label = QLabel("❌ Incorrect")
        incorrect_label.setStyleSheet("color: #abb2bf; font-size: 14px;")
        incorrect_value = QLabel(str(self.incorrect_chars))
        incorrect_value.setFont(QFont("Arial", 16, QFont.Bold))
        incorrect_value.setStyleSheet("color: #e06c75;")
        stats_layout.addWidget(incorrect_label, 2, 2)
        stats_layout.addWidget(incorrect_value, 3, 2)
        
        main_layout.addWidget(stats_frame)
        
        # Rating
        rating_frame = QFrame()
        rating_frame.setStyleSheet("""
            QFrame {
                background-color: #282c34;
                border-radius: 8px;
                margin: 10px;
                padding: 10px;
            }
        """)
        rating_layout = QVBoxLayout()
        rating_frame.setLayout(rating_layout)
        
        rating_label = QLabel(self.get_rating())
        rating_label.setAlignment(Qt.AlignCenter)
        rating_label.setFont(QFont("Arial", 16, QFont.Bold))
        rating_label.setStyleSheet(self.get_rating_color())
        rating_layout.addWidget(rating_label)
        
        main_layout.addWidget(rating_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        retry_button = QPushButton("🔄 Try Again")
        retry_button.setFont(QFont("Arial", 12, QFont.Bold))
        retry_button.setStyleSheet("""
            QPushButton {
                background-color: #61afef;
                color: #282c34;
                border: none;
                border-radius: 5px;
                padding: 10px 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #528bff;
            }
        """)
        retry_button.clicked.connect(self.accept)
        
        close_button = QPushButton("✖ Close")
        close_button.setFont(QFont("Arial", 12, QFont.Bold))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #e06c75;
                color: #282c34;
                border: none;
                border-radius: 5px;
                padding: 10px 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d45a63;
            }
        """)
        close_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(retry_button)
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
    
    def get_rating(self) -> str:
        """Get rating based on WPM and accuracy"""
        if self.wpm >= 80 and self.accuracy >= 95:
            return "🏆 Excellent! Professional typist level!"
        elif self.wpm >= 60 and self.accuracy >= 90:
            return "⭐ Great! You're an advanced typist!"
        elif self.wpm >= 40 and self.accuracy >= 85:
            return "👍 Good! You're an intermediate typist."
        elif self.wpm >= 30 and self.accuracy >= 75:
            return "📈 Fair. Keep practicing to improve!"
        else:
            return "💪 Keep practicing! You'll get better!"
    
    def get_rating_color(self) -> str:
        """Get color for rating text"""
        if self.wpm >= 80 and self.accuracy >= 95:
            return "color: #98c379;"
        elif self.wpm >= 60 and self.accuracy >= 90:
            return "color: #61afef;"
        elif self.wpm >= 40 and self.accuracy >= 85:
            return "color: #e5c07b;"
        elif self.wpm >= 30 and self.accuracy >= 75:
            return "color: #c678dd;"
        else:
            return "color: #e06c75;"
