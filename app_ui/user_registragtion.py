from PySide2.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                               QSpacerItem, QComboBox)
from models.database_models import User
from models.database_config import get_db, engine
from models.database_models import Base
from PySide2.QtCore import Qt
import re
import sys
import uuid


class UserRegistrationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration")
        self.setMinimumSize(350, 500)
        self.setMaximumSize(350, 500)
        self.db = next(get_db())

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Set a smaller spacing value
        layout.setAlignment(Qt.AlignCenter)  # Align the layout to the center horizontally

        # Add a spacer item for the top margin
        top_spacer = QSpacerItem(20, 20)
        layout.addItem(top_spacer)

        first_name_label = QLabel("First Name:")
        self.first_name_field = QLineEdit()
        self.first_name_field.setFixedWidth(250)
        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_field)

        last_name_label = QLabel("Last Name:")
        self.last_name_field = QLineEdit()
        self.last_name_field.setFixedWidth(250)
        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_field)

        email_label = QLabel("Email:")
        self.email_field = QLineEdit()
        self.email_field.setFixedWidth(250)
        layout.addWidget(email_label)
        layout.addWidget(self.email_field)

        password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setFixedWidth(250)
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_field)

        user_type_label = QLabel("User Type:")
        self.user_type_field = QComboBox()
        self.user_type_field.setFixedWidth(250)
        layout.addWidget(user_type_label)
        layout.addWidget(self.user_type_field)
        self.user_type_list()

        created_by_label = QLabel("Created By:")
        self.created_by_field = QLineEdit()
        self.created_by_field.setFixedWidth(250)
        layout.addWidget(created_by_label)
        layout.addWidget(self.created_by_field)

        spacer_item = QSpacerItem(20, 20)
        layout.addItem(spacer_item)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def user_type_list(self):
        user_list = ['0', '1']
        self.user_type_field.addItems(user_list)

    def register(self):
        first_name = self.first_name_field.text()
        last_name = self.last_name_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        user_type = self.user_type_field.currentText()
        created_by = self.created_by_field.text()

        if not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if not all([first_name, last_name, email, password]):
            QMessageBox.warning(self, "Missing Fields", "Please fill in all the required fields.")
            return

        if len(password) < 5:
            QMessageBox.warning(self, "Weak Password", "Password should be at least 5 characters long.")
            return

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            token=uuid.uuid4().hex,
            user_type=int(user_type),
            created_by=int(created_by) if created_by else 0
        )

        self.db.add(user)

        try:
            QMessageBox.information(self, "Registration Successful", "User created successfully.")
            # self.accept()
            self.db.commit()
            sys.exit(0)

        except Exception as e:
            print(e)
            QMessageBox.information(self, "Registration Error", "Something went wrong.")
            sys.exit(0)

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
    # Base.metadata.create_all(bind=engine)
    app = QApplication(sys.argv)

    registration_window = UserRegistrationWindow()
    registration_window.show()
    sys.exit(app.exec_())
