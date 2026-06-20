"""
Typing Speed Test - Main Application Window
Handles the UI and game logic
"""

import random
import time
import json
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QMessageBox,
    QFrame, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPalette
from word_generator import WordGenerator
from results_dialog import ResultsDialog


class TypingSpeedTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.word_generator = WordGenerator()
        self.current_words = []
        self.current_word_index = 0
        self.start_time = None
        self.end_time = None
        self.is_test_running = False
        self.characters_typed = 0
        self.correct_characters = 0
        self.incorrect_characters = 0
        self.time_limit = 60  # seconds
        self.time_remaining = 60
        
        # Timer for countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # Timer for typing delay
        self.typing_timer = QTimer()
        self.typing_timer.setSingleShot(True)
        self.typing_timer.timeout.connect(self.check_typing)
        
        self.init_ui()
        self.new_test()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("⌨️ Typing Speed Test")
        self.setMinimumSize(800, 600)
        
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 44, 52))
        self.setPalette(palette)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header_label = QLabel("⌨️ Typing Speed Test")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #abb2bf;")
        main_layout.addWidget(header_label)

        # Stats bar
        stats_layout = QHBoxLayout()
        
        self.wpm_label = QLabel("WPM: 0")
        self.wpm_label.setStyleSheet("color: #61afef; font-size: 16px; font-weight: bold;")
        
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.accuracy_label.setStyleSheet("color: #98c379; font-size: 16px; font-weight: bold;")
        
        self.time_label = QLabel(f"Time: {self.time_remaining}s")
        self.time_label.setStyleSheet("color: #e5c07b; font-size: 16px; font-weight: bold;")
        
        self.chars_label = QLabel("Chars: 0/0")
        self.chars_label.setStyleSheet("color: #c678dd; font-size: 16px; font-weight: bold;")
        
        stats_layout.addWidget(self.wpm_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.accuracy_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.time_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.chars_label)
        
        main_layout.addLayout(stats_layout)

        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Courier", 18))
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: #282c34;
                color: #abb2bf;
                border: 2px solid #3e4451;
                border-radius: 8px;
                padding: 15px;
                selection-background-color: #3e4451;
            }
        """)
        self.text_display.setMinimumHeight(200)
        main_layout.addWidget(self.text_display)

        # Input area
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("Start typing here...")
        self.input_area.setFont(QFont("Courier", 18))
        self.input_area.setStyleSheet("""
            QTextEdit {
                background-color: #1e222a;
                color: #abb2bf;
                border: 2px solid #3e4451;
                border-radius: 8px;
                padding: 15px;
            }
            QTextEdit:focus {
                border: 2px solid #61afef;
            }
        """)
        self.input_area.setMinimumHeight(100)
        self.input_area.textChanged.connect(self.on_text_changed)
        self.input_area.installEventFilter(self)
        main_layout.addWidget(self.input_area)

        # Control buttons
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("▶ Start Test")
        self.start_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #61afef;
                color: #282c34;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #528bff;
            }
            QPushButton:pressed {
                background-color: #3a6eb0;
            }
        """)
        self.start_button.clicked.connect(self.start_test)
        
        self.reset_button = QPushButton("🔄 New Test")
        self.reset_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e06c75;
                color: #282c34;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d45a63;
            }
            QPushButton:pressed {
                background-color: #b84a52;
            }
        """)
        self.reset_button.clicked.connect(self.reset_test)
        
        control_layout.addStretch()
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.reset_button)
        control_layout.addStretch()
        
        main_layout.addLayout(control_layout)

        # Status bar
        self.status_label = QLabel("Press 'Start Test' to begin")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #abb2bf; font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.status_label)

        # Set focus policy
        self.input_area.setFocusPolicy(Qt.StrongFocus)

    def eventFilter(self, obj, event):
        """Handle key events for the input area"""
        if obj == self.input_area and event.type() == QEvent.KeyPress:
            if self.is_test_running:
                # Allow typing
                return False
            else:
                # Block typing when test is not running
                if event.key() not in [Qt.Key_Tab, Qt.Key_Shift, Qt.Key_Control, 
                                      Qt.Key_Alt, Qt.Key_Meta, Qt.Key_CapsLock]:
                    event.ignore()
                    return True
        return super().eventFilter(obj, event)

    def new_test(self):
        """Generate new text for the test"""
        self.current_words = self.word_generator.generate_paragraph()
        self.current_word_index = 0
        self.display_text()
        
        # Reset stats
        self.characters_typed = 0
        self.correct_characters = 0
        self.incorrect_characters = 0
        self.time_remaining = self.time_limit
        self.time_label.setText(f"Time: {self.time_remaining}s")
        self.update_stats()

    def display_text(self):
        """Display the text to be typed"""
        self.text_display.clear()
        cursor = self.text_display.textCursor()
        
        for word in self.current_words:
            cursor.insertText(word + " ")
        
        # Reset cursor to beginning
        cursor.movePosition(QTextCursor.Start)
        self.text_display.setTextCursor(cursor)

    def highlight_current_word(self):
        """Highlight the current word in the display"""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.Start)
        
        # Move to current word
        for _ in range(self.current_word_index):
            cursor.movePosition(QTextCursor.NextWord)
        
        # Select the word
        cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
        self.text_display.setTextCursor(cursor)
        
        # Apply highlight
        char_format = cursor.charFormat()
        char_format.setBackground(QColor(61, 174, 233, 50))
        cursor.mergeCharFormat(char_format)
        
        # Move cursor back to start
        cursor.movePosition(QTextCursor.Start)
        self.text_display.setTextCursor(cursor)

    def start_test(self):
        """Start the typing test"""
        if self.is_test_running:
            return
            
        self.is_test_running = True
        self.start_time = time.time()
        self.start_button.setEnabled(False)
        self.input_area.setReadOnly(False)
        self.input_area.clear()
        self.input_area.setFocus()
        self.status_label.setText("⏱️ Test in progress... Type the text above")
        
        # Start the timer
        self.timer.start(1000)  # Update every second

    def reset_test(self):
        """Reset the test"""
        self.is_test_running = False
        self.timer.stop()
        self.start_time = None
        self.end_time = None
        self.start_button.setEnabled(True)
        self.input_area.setReadOnly(True)
        self.input_area.clear()
        self.status_label.setText("Press 'Start Test' to begin")
        
        # Reset display
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: #282c34;
                color: #abb2bf;
                border: 2px solid #3e4451;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        self.new_test()

    def on_text_changed(self):
        """Handle text input changes"""
        if not self.is_test_running:
            return
        
        # Start the typing timer to delay processing
        self.typing_timer.start(100)  # Wait 100ms for typing to stabilize

    def check_typing(self):
        """Process the typed text"""
        if not self.is_test_running:
            return
            
        typed_text = self.input_area.toPlainText()
        words = typed_text.strip().split()
        
        if not words:
            return
            
        # Check current word
        if self.current_word_index < len(self.current_words):
            current_word = self.current_words[self.current_word_index]
            typed_word = words[0] if words else ""
            
            # Update display colors
            self.highlight_current_word()
            
            # Check if word is complete
            if len(typed_word) >= len(current_word) and typed_text.endswith(" "):
                # Move to next word
                self.current_word_index += 1
                self.input_area.clear()
                
                # Check if all words are typed
                if self.current_word_index >= len(self.current_words):
                    self.end_test()
                    return
            
            # Update stats
            self.update_stats()

    def update_stats(self):
        """Update statistics display"""
        typed_text = self.input_area.toPlainText()
        
        # Calculate characters
        full_text = " ".join(self.current_words)
        typed_chars = typed_text.replace(" ", "")
        
        # Count correct characters
        correct = 0
        min_len = min(len(typed_chars), len(full_text))
        for i in range(min_len):
            if i < len(typed_chars) and i < len(full_text):
                if typed_chars[i] == full_text[i]:
                    correct += 1
        
        self.correct_characters = correct
        self.incorrect_characters = len(typed_chars) - correct
        self.characters_typed = len(typed_chars)
        
        # Calculate WPM
        elapsed_time = (time.time() - self.start_time) / 60 if self.start_time else 0
        if elapsed_time > 0:
            wpm = (self.correct_characters / 5) / elapsed_time
            self.wpm_label.setText(f"WPM: {int(wpm)}")
        
        # Calculate accuracy
        if self.characters_typed > 0:
            accuracy = (self.correct_characters / self.characters_typed) * 100
            self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
        
        # Update chars label
        self.chars_label.setText(f"Chars: {self.correct_characters}/{self.characters_typed}")

    def update_timer(self):
        """Update the countdown timer"""
        self.time_remaining -= 1
        self.time_label.setText(f"Time: {self.time_remaining}s")
        
        if self.time_remaining <= 0:
            self.end_test()

    def end_test(self):
        """End the typing test and show results"""
        self.is_test_running = False
        self.timer.stop()
        self.end_time = time.time()
        self.input_area.setReadOnly(True)
        self.start_button.setEnabled(True)
        
        # Calculate final stats
        total_time = self.end_time - self.start_time
        words_typed = self.current_word_index
        wpm = int((self.correct_characters / 5) / (total_time / 60))
        
        # Calculate accuracy
        total_chars = self.correct_characters + self.incorrect_characters
        accuracy = (self.correct_characters / total_chars * 100) if total_chars > 0 else 0
        
        self.status_label.setText("✅ Test completed!")
        
        # Show results dialog
        results = ResultsDialog(
            wpm,
            accuracy,
            total_chars,
            self.correct_characters,
            self.incorrect_characters,
            self.current_word_index,
            len(self.current_words)
        )
        results.exec_()
        
        # Reset after dialog is closed
        self.reset_test()

    def keyPressEvent(self, event):
        """Handle key press events globally"""
        if event.key() == Qt.Key_Escape and self.is_test_running:
            self.end_test()
        super().keyPressEvent(event)
