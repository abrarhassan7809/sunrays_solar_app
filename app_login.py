from PySide2.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QMessageBox, QSpacerItem, QWidget, QSizePolicy)
from PySide2.QtCore import Qt
from app_ui import user_registragtion
from models.database_models import User
from models.database_config import get_db
from app_ui.app_main_windwo import MainWindow
import sys
import re


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setMinimumSize(300, 400)
        self.setMaximumSize(300, 400)
        self.db = next(get_db())
        self.user = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Set a smaller spacing value

        # Add a spacer item for the top margin
        top_spacer = QSpacerItem(20, 60)
        main_layout.addItem(top_spacer)

        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(10)  # Set a smaller spacing value

        email_label = QLabel("Email:")
        self.email_field = QLineEdit()
        self.email_field.setFixedWidth(250)
        fields_layout.addWidget(email_label)
        fields_layout.addWidget(self.email_field)

        password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setFixedWidth(250)
        self.password_field.setEchoMode(QLineEdit.Password)
        fields_layout.addWidget(password_label)
        fields_layout.addWidget(self.password_field)

        fields_container = QWidget()
        fields_container_layout = QHBoxLayout(fields_container)
        fields_container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        fields_container_layout.addLayout(fields_layout)
        fields_container_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addWidget(fields_container)

        # Add a vertical spacer item to increase the space between password field and login button
        spacer_item = QSpacerItem(20, 40)
        main_layout.addItem(spacer_item)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        main_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        main_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        main_layout.addStretch()  # Add a stretchable space at the end to push the widgets to the top

        self.setLayout(main_layout)

    def login(self):
        email = self.email_field.text()
        password = self.password_field.text()

        if not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if len(password) < 5:
            QMessageBox.warning(self, "Invalid Password", "Password must be at least 5 characters.")
            return

        self.user = self.db.query(User).filter(User.email == email, User.password == password).first()

        if self.user:
            # QMessageBox.information(self, "Login Successful", "Login successful.")
            self.accept()
            self.user.active = True
            self.db.commit()

        else:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def register(self):
        user_register = user_registragtion.UserRegistrationWindow()
        user_register.exec_()

    def validate_email(self, email):
        # Simple email validation using regular expression
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            app.quit()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        main_window = MainWindow(login_window.user.token)
        main_window.show()
    else:
        sys.exit(0)

    sys.exit(app.exec_())
