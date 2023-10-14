import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog, QVBoxLayout, QWidget, QProgressBar, QAction, QStatusBar, QMenuBar
from PyQt5.QtGui import QKeySequence, QCursor, QFont, QPixmap, QIcon, QColor
from bs4 import BeautifulSoup
import requests
import urllib.parse
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class WebContentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Code Fetcher")
        self.setWindowIcon(QIcon(r"..\Images\123.ico"))
        self.setFixedSize(800, 600)  # Increased window size
        self.initUI()

    def initUI(self):
        # Apply a style sheet for a professional look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit, QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #005c99;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                font-family: Arial, sans-serif;
                font-size: 12px;
                color: #333333;
                padding: 4px;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }
        """)

        # Create a menu bar
        menubar = self.menuBar()

        # Create a "File" menu
        file_menu = menubar.addMenu("File")

        # Create an "Exit" action in the "File" menu
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)  # Keyboard shortcut to exit (e.g., Ctrl+Q)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create a "Help" menu
        help_menu = menubar.addMenu("Help")

        # Create a "How to Use" action in the "Help" menu
        how_to_use_action = QAction("How to Use", self)
        how_to_use_action.triggered.connect(self.show_help_dialog)
        help_menu.addAction(how_to_use_action)

        # URL label and input field
        self.url_label = QLabel("Enter URL:", self)
        # Set the text color to red
        self.url_label.setStyleSheet("color: #c7c7c7;")
        self.url_label.move(20, 30)
        self.url_label.setFont(QFont("Arial", 14))
        self.url_entry = QLineEdit(self)
        self.url_entry.setGeometry(140, 30, 460, 34)
        self.url_entry.setText("https://")
        self.url_entry.setFont(QFont("Arial", 12))
        self.url_entry.setToolTip("Enter the URL you want to fetch")

        # Fetch button with tooltip and keyboard shortcut (Alt + F)
        self.fetch_button = QPushButton("Fetch Content", self)
        self.fetch_button.setGeometry(620, 30, 120, 34)
        self.fetch_button.setFont(QFont("Arial", 12))
        self.fetch_button.setToolTip("Click to fetch content from the entered URL")
        self.fetch_button.setShortcut("Alt+F")
        self.fetch_button.clicked.connect(self.fetch_content)

        # Save button with tooltip and keyboard shortcut (Alt + S)
        self.save_button = QPushButton("Save Content", self)
        self.save_button.setGeometry(20, 540, 120, 30)
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.setToolTip("Click to save the fetched content to a file")
        self.save_button.setShortcut("Alt+S")
        self.save_button.setEnabled(False)  # Disable initially
        self.save_button.clicked.connect(self.save_content)

        # Clear button with tooltip and keyboard shortcut (Alt + C)
        self.clear_button = QPushButton("Clear Content", self)
        self.clear_button.setGeometry(160, 540, 120, 30)
        self.clear_button.setFont(QFont("Arial", 12))
        self.clear_button.setToolTip("Click to clear the content area")
        self.clear_button.setShortcut("Alt+C")
        self.clear_button.clicked.connect(self.clear_content)

        # Content display
        self.content_text = QTextEdit(self)
        self.content_text.setGeometry(20, 70, 760, 460)
        self.content_text.setReadOnly(True)  # Make it read-only
        self.content_text.setFont(QFont("Arial", 12))

        # Progress indicator
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(300, 540, 480, 30)
        self.progress_bar.setVisible(False)

        # Status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setFont(QFont("Arial", 12))
        self.status_bar.showMessage("Ready")  # Initial message
        self.status_bar.setSizeGripEnabled(False)  # Disable resizing

        # Change the background color of the status bar
        self.status_bar.setStyleSheet("color: green;")

        # Initialize the thread for fetching content
        self.fetch_thread = FetchContentThread()
        self.fetch_thread.content_fetched.connect(self.display_content)
        self.fetch_thread.error_occurred.connect(self.display_error)
        self.fetch_thread.progress_updated.connect(self.update_progress)

    def fetch_content(self):
        url = self.url_entry.text()

        # Validate the URL format
        if not self.is_valid_url(url):
            self.status_bar.showMessage("Invalid URL format. Please enter a valid URL.", 5000)
            return

        # Start the fetching thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)  # Set range from 0 to 100 for percentage
        self.status_bar.showMessage("Fetching content...")
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
        self.status_bar.showMessage("Content fetched successfully.", 5000)

    def display_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 1)  # Reset progress
        self.status_bar.showMessage(error_message, 5000)

    def save_content(self):
        content = self.content_text.toPlainText()
        if not content:
            self.status_bar.showMessage("No content to save.", 5000)
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save HTML Content", "", "HTML Files (*.html);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(content)
                QMessageBox.information(self, "Success", "Content saved successfully.")
                self.status_bar.showMessage("Content saved successfully.", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save content: {e}")
                self.status_bar.showMessage(f"Could not save content: {e}", 5000)

    def clear_content(self):
        self.content_text.clear()
        self.save_button.setEnabled(False)  # Disable the save button when content is cleared
        self.status_bar.showMessage("Content cleared.", 5000)

    def is_valid_url(self, url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def update_progress(self, percentage):
        self.progress_bar.setValue(percentage)

    def show_help_dialog(self):
        help_text = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    color: #333333;
                    background-color: #f0f0f0; /* Background color matching your app */
                    padding: 20px; /* Add some padding for spacing */
                }
                h1 {
                    font-size: 18px; /* Larger font size for headings */
                    color: #007acc; /* Custom primary color */
                    margin-bottom: 15px; /* Increased margin for spacing */
                }
                p {
                    margin: 10px 0;
                }
                ol, ul {
                    margin: 10px 0;
                    padding-left: 20px;
                }
                strong {
                    color: #005c99; /* Custom secondary color for strong text */
                }
                em {
                    font-style: italic; /* Italicize emphasized text */
                }
            </style>
        </head>
        <body>

        <p style="text-align: center;"><h2><span style="color: #007BFF;">===================================</span></h2>
        <h1>🛠 HTML Code Fetcher 🛠</h1>
        <h2>📝 Version: 1.4</h2>
        <h2>📅 Release Date: October 15, 2023</h2>
        <h2><span style="color: #007BFF;">===================================</span></h2></p>
        <p><h3>Welcome to <strong>HTML Code Fetcher!</strong> Follow these steps to use the application:</h3></p>
        <ol>
            <li>Enter the URL you want to fetch in the URL input field.</li>
            <li>Click the <strong>"Fetch Content"</strong> button to retrieve HTML content from the URL.</li>
            <li>The fetched content will be displayed in the text area below.</li>
            <li>You can save the fetched content using the <strong>"Save Content"</strong> button.</li>
            <li>To clear the content area, click the <strong>"Clear Content"</strong> button.</li>
        </ol>
            <p><em>Note:</em> Make sure to enter a valid URL and use the provided keyboard shortcuts for quick actions.</p>
        <p><strong>That's it!</strong>...Thank you for using <span style="color: #007BFF;">HTML Code Fetcher!</span>!</p>
 
        <!-- Add an image here -->
        <p style="text-align: center;"><img src="..\Images\htmlcodefetcher.png" alt="Sample-Logo1" width="150" height="100" border="1"></p>

        <p style="text-align: center;"><h3>▲▲▲👽👽 MY CHANNELS 👽👽▲▲▲</h3></p>
        <p style="text-align: center;"><a href="https://github.com/pudszttiot">Github Page</a></p>
        <p style="text-align: center;"><a href="https://youtube.com/channel/UCwtvRlFsh1-CI1h0g32AlwQ">YouTube Page</a></p>

    
        </body>
        </html>
        """

        # Create a QMessageBox to display HTML content
        show_help_dialog = QMessageBox()
        show_help_dialog.setWindowTitle("Help")
        
        show_help_dialog.setText(help_text)
        show_help_dialog.setTextFormat(Qt.RichText)
        # how_to_use_dialog.setFont(QFont("Arial", 12))
        show_help_dialog.setWindowIcon(QIcon(r"..\Images\123.ico"))
        show_help_dialog.exec_()

class FetchContentThread(QThread):
    content_fetched = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)  # Signal for live progress updates

    def __init__(self):
        super().__init__()
        self.url = ""

    def set_url(self, url):
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            total_length = len(response.content)
            content = response.text
            received_bytes = 0

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    received_bytes += len(chunk)
                    progress = int((received_bytes / total_length) * 100)
                    self.progress_updated.emit(progress)  # Emit progress signal
            self.content_fetched.emit(content)
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Could not fetch content from URL: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebContentApp()
    window.show()
    sys.exit(app.exec_())
