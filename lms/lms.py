import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QFormLayout,
    QDialog,
)
from PyQt5.QtCore import Qt
import sqlite3


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE
            )
            """
        )
        self.conn.commit()

    def add_book(self, title, author, isbn):
        self.cursor.execute(
            "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
            (title, author, isbn),
        )
        self.conn.commit()

    def edit_book(self, book_id, title, author, isbn):
        self.cursor.execute(
            "UPDATE books SET title=?, author=?, isbn=? WHERE id=?",
            (title, author, isbn, book_id),
        )
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()

    def get_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def search_books(self, query):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        return self.cursor.fetchall()


class AddEditDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Book")
        self.book = book

        self.layout = QFormLayout(self)

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()

        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Author:", self.author_input)
        self.layout.addRow("ISBN:", self.isbn_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.layout.addRow(self.save_button)

        if self.book:
            self.title_input.setText(self.book[1])
            self.author_input.setText(self.book[2])
            self.isbn_input.setText(self.book[3])

    def get_data(self):
        return (
            self.title_input.text(),
            self.author_input.text(),
            self.isbn_input.text(),
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        self.db = DatabaseManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by title, author, or ISBN...")
        self.search_bar.textChanged.connect(self.search_books)
        self.layout.addWidget(self.search_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # Buttons
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Book")
        self.edit_button.clicked.connect(self.edit_book)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Book")
        self.delete_button.clicked.connect(self.delete_book)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.load_books()

    def load_books(self):
        self.table.setRowCount(0)
        books = self.db.get_all_books()
        for row_number, book in enumerate(books):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(book):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search_books(self):
        query = self.search_bar.text()
        books = self.db.search_books(query)
        self.table.setRowCount(0)
        for row_number, book in enumerate(books):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(book):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_book(self):
        dialog = AddEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, author, isbn = dialog.get_data()
            self.db.add_book(title, author, isbn)
            self.load_books()

    def edit_book(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a book to edit.")
            return

        book_id = int(self.table.item(selected_row, 0).text())
        book = self.db.get_all_books()[selected_row]

        dialog = AddEditDialog(self, book)
        if dialog.exec_() == QDialog.Accepted:
            title, author, isbn = dialog.get_data()
            self.db.edit_book(book_id, title, author, isbn)
            self.load_books()

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a book to delete.")
            return

        book_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm", "Are you sure you want to delete this book?", QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.db.delete_book(book_id)
            self.load_books()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())