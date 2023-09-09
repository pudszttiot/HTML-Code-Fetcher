import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests

class WebContentApp:
    """
    A simple GUI application for fetching and selecting web content.
    """
    def __init__(self, root):
        """
        Initialize the application.
        """
        self.root = root
        self.root.title("Web Content Fetcher")
        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the application.
        """
        # URL entry
        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        # Fetch button
        self.fetch_button = tk.Button(self.root, text="Fetch Content", command=self.fetch_content)
        self.fetch_button.pack()

        # Content display
        self.content_text = tk.Text(self.root)
        self.content_text.pack()

    def fetch_content(self):
        """
        Fetch the content from the entered URL.
        """
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Could not fetch content from URL: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert(tk.END, soup.prettify())

if __name__ == "__main__":
    root = tk.Tk()
    app = WebContentApp(root)
    root.mainloop()
