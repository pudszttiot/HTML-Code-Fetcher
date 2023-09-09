import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog, QVBoxLayout, QWidget, QProgressBar
from bs4 import BeautifulSoup
import requests
import urllib.parse
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os

class WebContentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Code Fetcher")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # URL label and input field
        self.url_label = QLabel("Enter URL:", self)
        self.url_label.move(20, 20)
        self.url_entry = QLineEdit(self)
        self.url_entry.setGeometry(120, 20, 400, 30)
        self.url_entry.setText("https://")

        # Fetch button
        self.fetch_button = QPushButton("Fetch Content", self)
        self.fetch_button.setGeometry(540, 20, 100, 30)
        self.fetch_button.clicked.connect(self.fetch_content)

        # Save button
        self.save_button = QPushButton("Save Content", self)
        self.save_button.setGeometry(20, 580, 100, 30)
        self.save_button.clicked.connect(self.save_content)
        self.save_button.setEnabled(False)  # Disable initially

        # Clear button
        self.clear_button = QPushButton("Clear Content", self)
        self.clear_button.setGeometry(140, 580, 100, 30)
        self.clear_button.clicked.connect(self.clear_content)

        # Content display
        self.content_text = QTextEdit(self)
        self.content_text.setGeometry(20, 70, 720, 500)
        self.content_text.setReadOnly(True)  # Make it read-only

        # Progress indicator
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(650, 580, 100, 30)
        self.progress_bar.setVisible(False)

        # Initialize the thread for fetching content
        self.fetch_thread = FetchContentThread()
        self.fetch_thread.content_fetched.connect(self.display_content)
        self.fetch_thread.error_occurred.connect(self.display_error)

    def fetch_content(self):
        url = self.url_entry.text()

        # Validate the URL format
        if not self.is_valid_url(url):
            QMessageBox.critical(self, "Error", "Invalid URL format. Please enter a valid URL.")
            return

        # Start the fetching thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Infinite progress
        self.fetch_thread.set_url(url)
        self.fetch_thread.start()

    def display_content(self, content):
        # Prettify the HTML content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        pretty_content = soup.prettify()

        self.content_text.setPlainText(pretty_content)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 1)  # Reset progress
        self.save_button.setEnabled(True)  # Enable the save button

    def display_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 1)  # Reset progress

    def save_content(self):
        content = self.content_text.toPlainText()
        if not content:
            QMessageBox.critical(self, "Error", "No content to save.")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save HTML Content", "", "HTML Files (*.html);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(content)
                QMessageBox.information(self, "Success", "Content saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save content: {e}")

    def clear_content(self):
        self.content_text.clear()
        self.save_button.setEnabled(False)  # Disable the save button when content is cleared

    def is_valid_url(self, url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

class FetchContentThread(QThread):
    content_fetched = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.url = ""

    def set_url(self, url):
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = response.text
            self.content_fetched.emit(content)
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Could not fetch content from URL: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebContentApp()
    window.show()
    sys.exit(app.exec_())
