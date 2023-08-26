from PySide2.QtWidgets import (QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
                               QStackedWidget, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy,
                               QComboBox, QAbstractItemView, QMenu)
from PySide2.QtCore import Qt
from functools import partial
from PySide2.QtGui import QIcon

from app_ui import cetagories
from app_ui.app_registration import AppRegistrationWindow
from app_ui.cetagories import (AddPanelDialog, AddAccessoriesDialog, AddLaborDialog, AddBatteryDialog,
                               AddFrameDialog, AddInverterDialog, AddCustomerDialog, AddDCCableDialog,
                               AddACCableDialog, AddInvoiceDialog, AddSupplierDialog, AddLaborPaidDialog,
                               AddExpanseDialog, BanksTransactionsDialog, BanksPaymentsDialog, AddProjectDialog)
from models.database_config import get_db
from models.database_models import (User, Panel, Inverter, ACCable, DCCable, Frame, Labor, Quotation, Battery,
                                    Accessories, QuotationItem, Expanse, Customer, Supplier, LaborPaid, Banks,
                                    BankTransaction, Projects)
import sys


class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.db = next(get_db())
        self.user = self.db.query(User).filter(User.token == self.token).first()
        self.init_ui()

        # Add the table_widget attribute
        self.table_widget = None

    def init_ui(self):
        self.setWindowTitle("Inventory System")
        self.setFixedSize(self.screen().size())
        self.setMinimumSize(900, 600)

        # Create menu bar
        menu_bar = self.menuBar()
        self.set_app_icon()

        file_save = QAction(QIcon('app_icons/save.svg'), "Save", self)
        file_save.setShortcut('Ctrl+S')
        file_exit = QAction(QIcon('app_icons/x.svg'), "Exit", self)
        file_exit.setShortcut('Ctrl+Q')
        file_exit.triggered.connect(self.close)

        # action_edit = QAction(QIcon('app_icons/save.svg'), "Edit", self)
        # action_edit.setShortcut('Ctrl+E')
        # action_help = QAction(QIcon('app_icons/save.svg'), "Help", self)
        # action_help.setShortcut('Ctrl+H')

        add_banks_payments = QAction(QIcon('app_icons/bank-svgrepo-com.svg'), "Add Payments", self)
        add_banks_payments.triggered.connect(self.add_banks_payments)

        banks_transactions = QAction(QIcon('app_icons/bank-svgrepo-com.svg'), "Banks Transactions", self)
        add_banks_payments.setShortcut('Ctrl+B')
        banks_transactions.triggered.connect(self.show_banks)

        profit_loss = QAction(QIcon('app_icons/icons8-profit-64.png'), "Profit & Loss", self)
        profit_loss.triggered.connect(self.show_profit_loss)

        # Add File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(file_save)
        file_menu.addAction(file_exit)

        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(add_banks_payments)
        view_menu.addAction(banks_transactions)
        view_menu.addAction(profit_loss)
        # edit_menu = menu_bar.addMenu("Edit")
        # help_menu = menu_bar.addMenu("Help")

        # Create the central widget
        central_widget = QWidget()

        # Create main layout for the central widget
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create layout for the left menu
        menu_layout = QVBoxLayout()
        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)

        # Move the left menu button to the top position
        menu_layout.setAlignment(Qt.AlignTop)

        # Create a dropdown list for menu items
        menu_combo = QComboBox()
        menu_layout.addWidget(menu_combo)

        project_button = QPushButton("Projects")
        menu_layout.addWidget(project_button)
        project_button.clicked.connect(self.show_project_expanse)

        supplier_button = QPushButton("Supplier")
        menu_layout.addWidget(supplier_button)
        supplier_button.clicked.connect(self.show_supplier)

        customer_button = QPushButton("Customers")
        menu_layout.addWidget(customer_button)
        customer_button.clicked.connect(self.show_customer)

        expanse_button = QPushButton("Expanse")
        menu_layout.addWidget(expanse_button)
        expanse_button.clicked.connect(self.show_expanse)

        invoices_button = QPushButton("Invoices")
        menu_layout.addWidget(invoices_button)
        invoices_button.clicked.connect(self.show_invoice)

        menu_items = [
            ("", ""),
            ("Panel", "app_icons/icons8-solar-panel-40.png"),
            ("Inverter", "app_icons/icons8-inverter-65.png"),
            ("Frame", "app_icons/icons8-frame-67.png"),
            ("AC-Cable", "app_icons/icons8-coil-48.png"),
            ("DC-Cable", "app_icons/icons8-coil-48.png"),
            ("Batteries", "app_icons/icons8-battery-64.png"),
            ("Accessories", "app_icons/icons8-cart-48.png"),
            ("Employee", "app_icons/business-people.png"),
            ("Employee Salary", "app_icons/salary.png"),
            ("Q-Item", "app_icons/icons8-quotation-64.png"),
        ]

        self.todo_stack = QStackedWidget()

        for item_text, icon_path in menu_items:
            menu_combo.addItem(QIcon(icon_path), item_text)
            menu_combo.activated.connect(partial(self.on_menu_item_clicked))

            todo_widget = QWidget()
            todo_layout = QVBoxLayout()
            todo_widget.setLayout(todo_layout)

            # ==========register===========
            # Create a custom title bar-like layout
            title_bar_layout = QHBoxLayout()
            title_bar_layout.setAlignment(Qt.AlignRight)
            title_bar_layout.setContentsMargins(0, 0, 0, 0)

            invoice_button = QPushButton("Invoice")
            title_bar_layout.addWidget(invoice_button)
            invoice_button.clicked.connect(self.add_invoice)

            register_button = QPushButton("Register")
            title_bar_layout.addWidget(register_button)
            register_button.clicked.connect(self.register_user)

            todo_layout.addLayout(title_bar_layout)
            # ==========register===========

            table_widget = QTableWidget()
            table_widget.horizontalHeader().setStretchLastSection(True)
            todo_layout.addWidget(table_widget)
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

            # Create button layout
            button_layout = QHBoxLayout()
            button_layout.setMargin(10)

            # Add spacer item to push buttons to the right side
            spacer_item = QWidget()
            spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            button_layout.addWidget(spacer_item)

            # Create the buttons
            create_button = QPushButton("Add Items")
            update_button = QPushButton("Update")
            delete_button = QPushButton("Delete")

            button_layout.addWidget(create_button)
            button_layout.addWidget(update_button)
            button_layout.addWidget(delete_button)

            todo_layout.addLayout(button_layout)

            create_button.clicked.connect(self.open_add_window)
            update_button.clicked.connect(self.update_data)
            delete_button.clicked.connect(self.delete_item)

            self.todo_stack.addWidget(todo_widget)

        # Add left menu and right todos to the main layout
        main_layout.addWidget(menu_widget)
        main_layout.addWidget(self.todo_stack)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Show the main window
        self.show()

    def set_app_icon(self):
        app_icon = QIcon("app_icons/401262_archlinux_icon.png")
        self.setWindowIcon(app_icon)

    # ===========update data==============
    def update_data(self):
        if self.user is not None:
            cetagories.UpdateItemDialog(self.db, self.todo_stack)
        else:
            QMessageBox.warning(self, "Error", "Please login first.")

    # ===========delete items==============
    def delete_item(self):
        if self.user is not None:
            current_index = self.todo_stack.currentIndex()
            todo_widget = self.todo_stack.widget(current_index)
            table_widget = todo_widget.findChild(QTableWidget)

            # Get the selected item
            selected_items = table_widget.selectedItems()

            # Check if an item is selected
            if not selected_items:
                QMessageBox.warning(self, "Error", "No item selected.")
                return

            # Get the row indexes of the selected items
            selected_rows = set()
            for item in selected_items:
                selected_rows.add(item.row())

            # Display a confirmation dialog
            confirmation = QMessageBox.question(
                self,
                "Confirmation",
                "Are you sure you want to delete the selected item(s)?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirmation == QMessageBox.Yes:
                for row in sorted(selected_rows, reverse=True):
                    item_id = table_widget.item(row, 0).text()
                    self.delete_item_from_database(current_index, int(item_id))
                    table_widget.removeRow(row)
                self.db.commit()
        else:
            QMessageBox.warning(self, "Error", "Please login first.")

    def delete_item_from_database(self, index, item_id):
        YourModel = None
        if index == 1:
            YourModel = Panel
        if index == 2:
            YourModel = Inverter
        if index == 3:
            YourModel = Frame
        if index == 4:
            YourModel = ACCable
        if index == 5:
            YourModel = DCCable
        if index == 6:
            YourModel = Battery
        if index == 7:
            YourModel = Accessories
        if index == 8:
            YourModel = Labor
        if index == 9:
            YourModel = LaborPaid
        try:
            item = self.db.query(YourModel).get(item_id)
            if item is not None:
                self.db.delete(item)
                self.db.commit()
                QMessageBox.information(self, 'Success', 'Item deleted successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Item not found.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

    # ===========menu items==============
    def on_menu_item_clicked(self, index):
        if index == self.todo_stack.currentIndex():
            return
        todo_widget = self.todo_stack.widget(index)
        table_widget = todo_widget.findChild(QTableWidget)

        if table_widget is None:
            table_widget = QTableWidget(todo_widget)
            todo_widget.layout().addWidget(table_widget)
        else:
            table_widget.clear()
        if index == 0:
            pass
        if index == 1:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Capacity", "Quantity", "Purchase Price",
                       "Sell Price"]
            db_data = self.db.query(Panel).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.capacity)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 2:
            headers = ["#",  "Product Code", "Product Name", "Brand", "Type", "Power Rating", "Quantity",
                       "Purchase Price", "Sell Price"]
            db_data = self.db.query(Inverter).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.power_rating)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 3:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Width", "Height", "Quantity",
                       "Purchase Price", "Sell Price"]
            db_data = self.db.query(Frame).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.width)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.height)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 9, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 4:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Size", "Quantity", "Purchase Price",
                       "Sell Price"]
            db_data = self.db.query(ACCable).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.size)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 5:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Size", "Quantity", "Purchase Price",
                       "Sell Price"]
            db_data = self.db.query(DCCable).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.size)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 6:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Warranty", "Capacity", "Voltage",
                       "Quantity", "Purchase Price", "Sell Price"]
            db_data = self.db.query(Battery).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.warranty)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.capacity)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.voltage)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 9, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 10, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 7:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Quantity", "Purchase Price",
                       "Sell Price"]
            db_data = self.db.query(Accessories).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.purchase_price)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.sell_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 8:
            headers = ["#", "Employee Name", "Start Date", "Phone Number", "Employee CNIC", "Address", "Total Salary"]
            db_data = self.db.query(Labor).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.labor_name)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.start_date)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.phon_number)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.labor_cnic)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.labor_address)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.labor_pay)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 9:
            headers = ["#", "Employee Name", "Employee CNIC", "Absent Days", "Present Days", "Remaining Salary",
                       "Last Paid"]
            db_data = self.db.query(LaborPaid).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.labor_name)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.labor_cnic)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.absent_days)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.present_days)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.remaining_pay)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.last_paid)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif index == 10:
            headers = ["#", "Product Code", "Product Name", "Brand", "Type", "Quantity", "Sell Price", "Total Price"]
            db_data = self.db.query(QuotationItem).all()

            # Set the new headers
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.product_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.product_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.brand)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.typ)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.quantity)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.sell_price)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.total_price)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Resize the columns to fit the content
        table_widget.resizeColumnsToContents()
        self.todo_stack.setCurrentIndex(index)

    # ===========registration==============
    def register_user(self):
        user_register = AppRegistrationWindow(self.user.id)
        user_register.exec_()

    # ===========profit loss==============
    def show_profit_loss(self):
        pass

    # ===========banks==============
    def show_banks(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            banks_dialog = BanksTransactionsDialog(self.db, self.user.id, table_widget)
            banks_dialog.exec_()

            headers = ["#", "Bank ID", "Account No", "Bank Name", "Description", "Amount", "Transaction Date"]
            db_data = self.db.query(BankTransaction).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 5)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.bank_id)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.account_number)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.bank_name)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.description)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.amount)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.transaction_date)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    def add_banks_payments(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            banks_dialog = BanksPaymentsDialog(self.db, self.user.id, table_widget)
            banks_dialog.exec_()

            headers = ["#", "User Name", "Account No", "Bank Name", "Amount", "Transaction Date"]
            db_data = self.db.query(Banks).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 5)

            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.user_name)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.account_number)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.bank_name)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.amount)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.transaction_date)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========supplier==========
    def show_supplier(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            add_invoice_dialog = AddSupplierDialog(self.db, self.user.id, table_widget)
            add_invoice_dialog.exec_()

            headers = ["#", "Supplier Name", "Company", "Phone Number", "Email", "Address"]
            db_data = self.db.query(Supplier).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            # Calculate the width of other columns
            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            # Set the width of other columns
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.supplier_name)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.company)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.phon_number)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.email)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.address)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========customer==========
    def show_customer(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            add_invoice_dialog = AddCustomerDialog(self.db, self.user.id, table_widget)
            add_invoice_dialog.exec_()

            headers = ["#", "Customer Name", "Company", "Phone Number", "Email", "City", "Address"]
            db_data = self.db.query(Customer).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            # Calculate the width of other columns
            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            # Set the width of other columns
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.customer_name)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.company)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.phone_number)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.email)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.city)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.address)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========expanse==========
    def show_expanse(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            add_expanse_dialog = AddExpanseDialog(self.db, self.user.id, table_widget)
            add_expanse_dialog.exec_()

            headers = ["#", "Description", "Amount", "Date"]
            db_data = self.db.query(Expanse).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            # Calculate the width of other columns
            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            # Set the width of other columns
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.description)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.amount)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.date)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========project expanse==========
    def show_project_expanse(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            add_expanse_dialog = AddProjectDialog(self.db, self.user.id, table_widget)
            add_expanse_dialog.exec_()

            headers = ["#", "Project Code", "Project Name", "Description", "Address", "Project Cost",
                       "Receiving Amount", "Remaining Amount", "Date"]
            db_data = self.db.query(Projects).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            # Calculate the width of other columns
            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            # Set the width of other columns
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.project_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.project_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.description)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.address)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.project_cost)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.receiving_amount)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.remaining_amount)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.date)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========invoice==========
    def show_invoice(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        headers = ["#", "Invoice Code", "Customer Name", "Walk in Customer", "Date", "Discount", "Grand Total",
                   "Receiving Amount", "Remaining Amount"]
        db_data = self.db.query(Quotation).all()

        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(db_data))
        table_widget.setColumnWidth(0, 10)

        # Calculate the width of other columns
        total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
        column_width = total_width // (len(headers) - 1)

        # Set the width of other columns
        for col in range(1, len(headers)):
            table_widget.setColumnWidth(col, column_width)

        for row, item in enumerate(db_data):
            table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
            table_widget.setItem(row, 1, QTableWidgetItem(str(item.invoice_code)))
            table_widget.setItem(row, 2, QTableWidgetItem(str(item.customer_name)))
            table_widget.setItem(row, 3, QTableWidgetItem(str(item.walk_in_customer)))
            table_widget.setItem(row, 4, QTableWidgetItem(str(item.date)))
            table_widget.setItem(row, 5, QTableWidgetItem(str(item.discount)))
            table_widget.setItem(row, 6, QTableWidgetItem(str(item.grand_total)))
            table_widget.setItem(row, 7, QTableWidgetItem(str(item.receiving_amount)))
            table_widget.setItem(row, 8, QTableWidgetItem(str(item.remaining_amount)))

        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def add_invoice(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user:
            add_invoice_dialog = AddInvoiceDialog(self.db, self.user.id, table_widget)
            add_invoice_dialog.exec_()

            headers = ["#", "Invoice Code", "Customer Name", "Walk in Customer", "Date", "Discount", "Grand Total",
                       "Receiving Amount", "Remaining Amount"]
            db_data = self.db.query(Quotation).all()

            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(db_data))
            table_widget.setColumnWidth(0, 10)

            # Calculate the width of other columns
            total_width = table_widget.viewport().width() - table_widget.columnWidth(0)
            column_width = total_width // (len(headers) - 1)

            # Set the width of other columns
            for col in range(1, len(headers)):
                table_widget.setColumnWidth(col, column_width)

            for row, item in enumerate(db_data):
                table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
                table_widget.setItem(row, 1, QTableWidgetItem(str(item.invoice_code)))
                table_widget.setItem(row, 2, QTableWidgetItem(str(item.customer_name)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(item.walk_in_customer)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item.date)))
                table_widget.setItem(row, 5, QTableWidgetItem(str(item.discount)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(item.grand_total)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(item.receiving_amount)))
                table_widget.setItem(row, 8, QTableWidgetItem(str(item.remaining_amount)))

            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        elif self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

    # =========inventory list==========
    def open_add_window(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if self.user is None:
            QMessageBox.warning(self, "Error", "Please login first.")

        elif current_index == 1:  # Panel
            add_panel_dialog = AddPanelDialog(self.db, self.user.id, table_widget)
            add_panel_dialog.exec_()

        elif current_index == 2:  # Inverter
            add_inverter_dialog = AddInverterDialog(self.db, self.user.id, table_widget)
            add_inverter_dialog.exec_()

        elif current_index == 3:  # Frame
            add_frame_dialog = AddFrameDialog(self.db, self.user.id, table_widget)
            add_frame_dialog.exec_()

        elif current_index == 4:  # AC-Cable
            add_ac_cable_dialog = AddACCableDialog(self.db, self.user.id, table_widget)
            add_ac_cable_dialog.exec_()

        elif current_index == 5:  # DC-Cable
            add_dc_cable_dialog = AddDCCableDialog(self.db, self.user.id, table_widget)
            add_dc_cable_dialog.exec_()

        elif current_index == 6:  # Battery
            add_battery_dialog = AddBatteryDialog(self.db, self.user.id, table_widget)
            add_battery_dialog.exec_()

        elif current_index == 7:  # Accessories
            add_accessories_dialog = AddAccessoriesDialog(self.db, self.user.id, table_widget)
            add_accessories_dialog.exec_()

        elif current_index == 8:    # Labor
            add_accessories_dialog = AddLaborDialog(self.db, self.user.id, table_widget)
            add_accessories_dialog.exec_()

        elif current_index == 9:    # Labor Salary
            add_accessories_dialog = AddLaborPaidDialog(self.db, self.user.id, table_widget)
            add_accessories_dialog.exec_()

    def handle_added_item(self, item_data):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)

        if all(item_data.values()):
            row_count = table_widget.rowCount()
            table_widget.insertRow(row_count)

            for column, data in enumerate(item_data.values()):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row_count, column, item)
        else:
            QMessageBox.warning(self, "Error", "All fields are required.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow('token')
    sys.exit(app.exec_())