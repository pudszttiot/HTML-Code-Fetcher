# homepage.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from main import WebContentApp

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Code Fetcher")
        self.setWindowIcon(QIcon(r"..\Images\123.ico"))
        self.setFixedSize(800, 600)  # Increased window size

        # Create a QLabel widget to display an animated GIF
        image_label = QLabel(self)
        image_label.setGeometry(400, -40, 550, 400)
        # Specify the path to the GIF file
        movie = QMovie(r"..\Images\animatedhtmlcodefetcher1.gif")
        
        image_label.setMovie(movie)
        # Calculate the center position for the label
        center_x = (self.width() - image_label.width()) // 2
        center_y = (self.height() - image_label.height()) // 3

        # Set the label position to the center
        image_label.move(center_x, center_y)

        # Start the GIF animation
        movie.start()


        # Create a button to open the content page
        self.open_button = QPushButton("Open HTML Code Fetcher", self)
        self.open_button.setGeometry(300, 480, 200, 50)
        self.open_button.clicked.connect(self.open_content_page)

        # Apply custom style to the button (same as before)
        self.open_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2E8B57;
                border: 1px solid #2980b9;
            }
            """
        )

    def open_content_page(self):
        # Open the content page frame (imported from your existing code)
        self.content_page = WebContentApp()
        self.content_page.show()

        # Close the home page
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set a custom application-wide style (optional)
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #000000;
        }
        """
    )

    homepage = HomePage()
    homepage.show()
    sys.exit(app.exec_())
