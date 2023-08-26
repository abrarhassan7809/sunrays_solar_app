from PySide2.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidgetItem, QDateEdit,
                               QTableWidget, QMessageBox, QComboBox, QHBoxLayout, QWidget, QHeaderView, QSizePolicy,
                               QGridLayout)
from sqlalchemy import and_

from models.database_models import (Panel, Frame, Inverter, Accessories, Labor, Battery, Quotation, QuotationItem,
                                    ACCable, DCCable, Customer, Supplier, LaborPaid, Expanse, Banks, BankTransaction,
                                    Projects)
from PySide2.QtPrintSupport import QPrinter, QPrintDialog
from PySide2.QtCore import QDate, Qt
from PySide2.QtGui import QTextDocument
import os


class AddInvoiceDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Invoice")
        self.setMinimumSize(1050, 600)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.invoice_code_label = QLabel("Invoice Code:")
        self.invoice_code_combobox = QComboBox()
        self.populate_invoice_code_combobox()

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_combobox = QComboBox()
        self.populate_customer_name_combobox()

        self.walk_in_customer_label = QLabel("Walk-in Customer:")
        self.walk_in_customer_combobox = QLineEdit()
        # self.populate_walk_in_customer_combobox()

        self.product_code_label = QLabel("Product Code:")
        self.product_code_edit = QLineEdit()
        self.product_code_edit.textChanged.connect(self.populate_product_code_combobox)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_combobox = QLineEdit()

        self.brand_label = QLabel("Brand:")
        self.brand_combobox = QLineEdit()

        self.type_label = QLabel("Type:")
        self.type_combobox = QLineEdit()

        self.quantity_label = QLabel("Quantity:")
        self.quantity_edit = QLineEdit()
        self.quantity_edit.textChanged.connect(self.calculate_total_price)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_edit = QLineEdit()

        self.total_price_label = QLabel("Total Price:")
        self.total_price_edit = QLineEdit()

        self.date_label = QLabel("Date:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())

        self.grand_total_label = QLabel("Grand Total:")
        self.grand_total_edit = QLineEdit()

        self.discount_label = QLabel("Discount:")
        self.discount_edit = QLineEdit()

        self.receiving_amount_label = QLabel("Receiving Amount:")
        self.receiving_amount_edit = QLineEdit()

        self.remaining_amount_label = QLabel("Remaining Amount:")
        self.remaining_amount_edit = QLineEdit()

        # Additional fields
        self.panel_quantity_label = QLabel("Panel Quantity:")
        self.panel_quantity_edit = QLineEdit()
        self.panel_quantity_edit.setReadOnly(True)

        self.inverter_quantity_label = QLabel("Inverter Quantity:")
        self.inverter_quantity_edit = QLineEdit()
        self.inverter_quantity_edit.setReadOnly(True)

        self.frame_quantity_label = QLabel("Frame Quantity:")
        self.frame_quantity_edit = QLineEdit()
        self.frame_quantity_edit.setReadOnly(True)

        self.ac_cables_label = QLabel("AC Cables:")
        self.ac_cables_edit = QLineEdit()
        self.ac_cables_edit.setReadOnly(True)

        self.dc_cables_label = QLabel("DC Cables:")
        self.dc_cables_edit = QLineEdit()
        self.dc_cables_edit.setReadOnly(True)

        self.battery_label = QLabel("Batteries:")
        self.battery_edit = QLineEdit()
        self.battery_edit.setReadOnly(True)

        header_layout.addWidget(self.invoice_code_label, 0, 0)
        header_layout.addWidget(self.invoice_code_combobox, 0, 1)
        header_layout.addWidget(self.customer_name_label, 0, 2)
        header_layout.addWidget(self.customer_name_combobox, 0, 3)
        header_layout.addWidget(self.walk_in_customer_label, 0, 4)
        header_layout.addWidget(self.walk_in_customer_combobox, 0, 5)
        header_layout.addWidget(self.product_code_label, 1, 0)
        header_layout.addWidget(self.product_code_edit, 1, 1)
        header_layout.addWidget(self.product_name_label, 1, 2)
        header_layout.addWidget(self.product_name_combobox, 1, 3)
        header_layout.addWidget(self.quantity_label, 2, 0)
        header_layout.addWidget(self.quantity_edit, 2, 1)
        header_layout.addWidget(self.type_label, 2, 2)
        header_layout.addWidget(self.type_combobox, 2, 3)
        header_layout.addWidget(self.sell_price_label, 3, 0)
        header_layout.addWidget(self.sell_price_edit, 3, 1)
        header_layout.addWidget(self.brand_label, 3, 2)
        header_layout.addWidget(self.brand_combobox, 3, 3)
        header_layout.addWidget(self.total_price_label, 4, 0)
        header_layout.addWidget(self.total_price_edit, 4, 1)
        header_layout.addWidget(self.date_label, 4, 2)
        header_layout.addWidget(self.date_edit, 4, 3)
        header_layout.addWidget(self.grand_total_label, 5, 0)
        header_layout.addWidget(self.grand_total_edit, 5, 1)
        header_layout.addWidget(self.discount_label, 5, 2)
        header_layout.addWidget(self.discount_edit, 5, 3)
        header_layout.addWidget(self.receiving_amount_label, 6, 0)
        header_layout.addWidget(self.receiving_amount_edit, 6, 1)
        header_layout.addWidget(self.remaining_amount_label, 6, 2)
        header_layout.addWidget(self.remaining_amount_edit, 6, 3)

        # Additional fields
        header_layout.addWidget(self.panel_quantity_label, 0, 6)
        header_layout.addWidget(self.panel_quantity_edit, 0, 7)
        header_layout.addWidget(self.inverter_quantity_label, 1, 6)
        header_layout.addWidget(self.inverter_quantity_edit, 1, 7)
        header_layout.addWidget(self.frame_quantity_label, 2, 6)
        header_layout.addWidget(self.frame_quantity_edit, 2, 7)
        header_layout.addWidget(self.ac_cables_label, 3, 6)
        header_layout.addWidget(self.ac_cables_edit, 3, 7)
        header_layout.addWidget(self.dc_cables_label, 4, 6)
        header_layout.addWidget(self.dc_cables_edit, 4, 7)
        header_layout.addWidget(self.battery_label, 5, 6)
        header_layout.addWidget(self.battery_edit, 5, 7)

        # Connect discount textChanged signal to update_grand_total slot
        self.discount_edit.textChanged.connect(self.update_grand_total)
        self.receiving_amount_edit.textChanged.connect(self.update_remaining_amount)

        # Create the body section
        headers = ["Customer Name", "Walk-in Customer", "Product Code", "Item", "Brand", "Type", "Quantity",
                   "Sell Price", "Total Price", "Date"]
        self.body_table = QTableWidget()
        self.body_table.setColumnCount(len(headers))
        self.body_table.setHorizontalHeaderLabels(headers)
        main_layout.addWidget(self.body_table)
        header = self.body_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the selection behavior to select entire rows
        self.body_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_window)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_from_invoice)
        self.create_invoice_button = QPushButton("Create Invoice")
        self.create_invoice_button.clicked.connect(self.create_invoice)
        # self.print_button = QPushButton("Print")
        # self.print_button.clicked.connect(self.print_invoice)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.create_invoice_button)
        # button_layout.addWidget(self.print_button)

        self.populate_quantities_fields()

    def populate_product_code_combobox(self):
        product_code = self.product_code_edit.text()
        db_panel = self.db.query(Panel).filter_by(product_code=product_code).first()
        db_inverter = self.db.query(Inverter).filter_by(product_code=product_code).first()
        db_frame = self.db.query(Frame).filter_by(product_code=product_code).first()
        db_ac_cable = self.db.query(ACCable).filter_by(product_code=product_code).first()
        db_dc_cable = self.db.query(DCCable).filter_by(product_code=product_code).first()
        db_battery = self.db.query(Battery).filter_by(product_code=product_code).first()
        db_accessories = self.db.query(Accessories).filter_by(product_code=product_code).first()
        if db_panel is not None:
            product_name = db_panel.product_name
            brand = db_panel.brand
            typ = db_panel.typ
            sell_price = db_panel.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_inverter is not None:
            product_name = db_inverter.product_name
            brand = db_inverter.brand
            typ = db_inverter.typ
            sell_price = db_inverter.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_frame is not None:
            product_name = db_frame.product_name
            brand = db_frame.brand
            typ = db_frame.typ
            sell_price = db_frame.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_ac_cable is not None:
            product_name = db_ac_cable.product_name
            brand = db_ac_cable.brand
            typ = db_ac_cable.typ
            sell_price = db_ac_cable.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_dc_cable is not None:
            product_name = db_dc_cable.product_name
            brand = db_dc_cable.brand
            typ = db_dc_cable.typ
            sell_price = db_dc_cable.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_battery is not None:
            product_name = db_battery.product_name
            brand = db_battery.brand
            typ = db_battery.typ
            sell_price = db_battery.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

        elif db_accessories is not None:
            product_name = db_accessories.product_name
            brand = db_accessories.brand
            typ = db_accessories.typ
            sell_price = db_accessories.sell_price
            self.product_name_combobox.setText(product_name)
            self.brand_combobox.setText(brand)
            self.type_combobox.setText(typ)
            self.sell_price_edit.setText(str(sell_price))

    def update_grand_total(self):
        total_price = 0
        for row in range(self.body_table.rowCount()):
            total_price_item = self.body_table.item(row, 7)
            if total_price_item:
                total_price += float(total_price_item.text())

        discount = self.discount_edit.text()

        if discount:
            discount_percentage = float(discount) / 100
            discount_amount = total_price * discount_percentage
            grand_total = total_price - discount_amount
        else:
            grand_total = total_price

        self.grand_total_edit.setText(str(grand_total))

    def update_remaining_amount(self):
        total_price = self.grand_total_edit.text()
        receiving_amount = self.receiving_amount_edit.text()

        if total_price and receiving_amount:
            remaining_amount = float(total_price) - float(receiving_amount)
            self.remaining_amount_edit.setText(str(remaining_amount))
        else:
            self.remaining_amount_edit.clear()

    def populate_invoice_code_combobox(self):
        code_list = ['SRS-02', 'SRS-03', 'SRS-04']
        self.invoice_code_combobox.addItems(code_list)

    def populate_customer_name_combobox(self):
        customers = ['']
        db_customer = self.db.query(Customer).all()
        if len(db_customer) >= 1:
            for custom in db_customer:
                customers.append(custom.customer_name)

        self.customer_name_combobox.addItems(customers)

    def populate_sell_price_combobox(self):
        product_code = self.product_code_edit.text()
        db_panel = self.db.query(Panel).filter_by(product_code=product_code).first()
        db_inverter = self.db.query(Inverter).filter_by(product_code=product_code).first()
        db_frame = self.db.query(Frame).filter_by(product_code=product_code).first()
        db_ac_cable = self.db.query(ACCable).filter_by(product_code=product_code).first()
        db_dc_cable = self.db.query(DCCable).filter_by(product_code=product_code).first()
        db_battery = self.db.query(Battery).filter_by(product_code=product_code).first()
        db_accessories = self.db.query(Accessories).filter_by(product_code=product_code).first()
        if db_panel is not None:
            if db_panel:
                self.sell_price_edit.setText(str(db_panel.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_inverter is not None:
            if db_inverter:
                self.sell_price_edit.setText(str(db_inverter.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_frame is not None:
            if db_frame:
                self.sell_price_edit.setText(str(db_frame.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_ac_cable is not None:
            if db_ac_cable:
                self.sell_price_edit.setText(str(db_ac_cable.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_dc_cable is not None:
            if db_dc_cable:
                self.sell_price_edit.setText(str(db_dc_cable.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_battery is not None:
            if db_battery:
                self.sell_price_edit.setText(str(db_battery.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

        elif db_accessories is not None:
            if db_accessories:
                self.sell_price_edit.setText(str(db_accessories.sell_price))
            else:
                self.sell_price_edit.setText(str(0))

    def calculate_total_price(self):
        quantity = self.quantity_edit.text()
        sell_price = self.sell_price_edit.text()

        if quantity and sell_price:
            total_price = int(quantity) * float(sell_price)
            self.total_price_edit.setText(str(total_price))

    def add_to_window(self):
        customer_name = self.customer_name_combobox.currentText()
        walk_in_customer = self.walk_in_customer_combobox.text()
        product_code = self.product_code_edit.text()
        product_name = self.product_name_combobox.text()
        brand = self.brand_combobox.text()
        typ = self.type_combobox.text()
        quantity = self.quantity_edit.text()
        sell_price = self.sell_price_edit.text()
        total_price = self.total_price_edit.text()
        date = self.date_edit.date().toString("yyyy-MM-dd")

        db_panel = self.db.query(Panel).filter_by(product_code=product_code).first()
        db_inverter = self.db.query(Inverter).filter_by(product_code=product_code).first()
        db_frame = self.db.query(Frame).filter_by(product_code=product_code).first()
        db_ac_cable = self.db.query(ACCable).filter_by(product_code=product_code).first()
        db_dc_cable = self.db.query(DCCable).filter_by(product_code=product_code).first()
        db_battery = self.db.query(Battery).filter_by(product_code=product_code).first()
        db_accessories = self.db.query(Accessories).filter_by(product_code=product_code).first()

        # Query the specific table based on the product name
        if db_panel is not None:
            if int(quantity) >= int(db_panel.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_panel.quantity} Quantities are remaining')
                return

        elif db_inverter is not None:
            if int(quantity) >= int(db_inverter.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_inverter.quantity} Quantities are remaining')
                return

        elif db_frame is not None:
            if int(quantity) >= int(db_frame.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_frame.quantity} Quantities are remaining')
                return

        elif db_ac_cable is not None:
            if int(quantity) >= int(db_ac_cable.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_ac_cable.quantity} Quantities are remaining')
                return

        elif db_dc_cable is not None:
            if int(quantity) >= int(db_dc_cable.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_dc_cable.quantity} Quantities are remaining')
                return

        elif db_battery is not None:
            if int(quantity) >= int(db_battery.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_battery.quantity} Quantities are remaining')
                return

        elif db_accessories is not None:
            if int(quantity) >= int(db_accessories.quantity):
                QMessageBox.warning(self, 'Warning', f'Only {db_accessories.quantity} Quantities are remaining')
                return
        else:
            QMessageBox.warning(self, "Warning", "Invalid product code")
            return

        row_count = self.body_table.rowCount()
        self.body_table.insertRow(row_count)

        self.body_table.setItem(row_count, 0, QTableWidgetItem(customer_name))
        self.body_table.setItem(row_count, 1, QTableWidgetItem(walk_in_customer))
        self.body_table.setItem(row_count, 2, QTableWidgetItem(product_code))
        self.body_table.setItem(row_count, 3, QTableWidgetItem(product_name))
        self.body_table.setItem(row_count, 4, QTableWidgetItem(brand))
        self.body_table.setItem(row_count, 5, QTableWidgetItem(typ))
        self.body_table.setItem(row_count, 6, QTableWidgetItem(quantity))
        self.body_table.setItem(row_count, 7, QTableWidgetItem(sell_price))
        self.body_table.setItem(row_count, 8, QTableWidgetItem(total_price))
        self.body_table.setItem(row_count, 9, QTableWidgetItem(date))

        self.calculate_grand_total_price()
        self.update_quantities(product_code, int(quantity))
        self.clear_product_fields()

    def update_quantities(self, item_code, quantity):
        db_panel = self.db.query(Panel).filter_by(product_code=item_code).first()
        db_inverter = self.db.query(Inverter).filter_by(product_code=item_code).first()
        db_frame = self.db.query(Frame).filter_by(product_code=item_code).first()
        db_ac_cable = self.db.query(ACCable).filter_by(product_code=item_code).first()
        db_dc_cable = self.db.query(DCCable).filter_by(product_code=item_code).first()
        db_battery = self.db.query(Battery).filter_by(product_code=item_code).first()
        db_accessories = self.db.query(Accessories).filter_by(product_code=item_code).first()

        if db_panel is not None:
            db_panel.quantity -= quantity
        elif db_inverter is not None:
            db_inverter.quantity -= quantity
        elif db_frame is not None:
            db_frame.quantity -= quantity
        elif db_ac_cable is not None:
            db_ac_cable.quantity -= quantity
        elif db_dc_cable is not None:
            db_dc_cable.quantity -= quantity
        elif db_battery is not None:
            db_battery.quantity -= quantity
        elif db_accessories is not None:
            db_accessories.quantity -= quantity

        self.populate_quantities_fields()

    def populate_quantities_fields(self):
        panel_quantity = self.get_total_quantity(Panel)
        inverter_quantity = self.get_total_quantity(Inverter)
        frame_quantity = self.get_total_quantity(Frame)
        ac_cables_quantity = self.get_total_quantity(ACCable)
        dc_cables_quantity = self.get_total_quantity(DCCable)
        battery_quantity = self.get_total_quantity(Battery)

        self.panel_quantity_edit.setText(str(panel_quantity))
        self.inverter_quantity_edit.setText(str(inverter_quantity))
        self.frame_quantity_edit.setText(str(frame_quantity))
        self.ac_cables_edit.setText(str(ac_cables_quantity))
        self.dc_cables_edit.setText(str(dc_cables_quantity))
        self.battery_edit.setText(str(battery_quantity))

    def get_total_quantity(self, model):
        quantity = 0
        items = self.db.query(model).all()
        for item in items:
            quantity += item.quantity
        return quantity

    def clear_product_fields(self):
        self.product_code_edit.clear()
        self.quantity_edit.clear()
        self.sell_price_edit.clear()
        self.total_price_edit.clear()

    def delete_from_invoice(self):
        selected_rows = set()
        product_code = None
        item_quantity = None

        for item in self.body_table.selectedItems():
            selected_rows.add(item.row())
            product_code = self.body_table.item(item.row(), 2).text()
            item_quantity = int(self.body_table.item(item.row(), 6).text())

        for row in sorted(selected_rows, reverse=True):
            self.body_table.removeRow(row)

        self.calculate_grand_total_price()
        self.update_quantities(product_code, -item_quantity)
        self.populate_quantities_fields()

    def calculate_grand_total_price(self):
        grand_total = 0
        for row in range(self.body_table.rowCount()):
            total_price_item = self.body_table.item(row, 8)
            if total_price_item:
                total_price = float(total_price_item.text())
                grand_total += total_price

        self.grand_total_edit.setText(str(grand_total))

    def create_invoice(self):
        if 0 >= self.body_table.rowCount():
            QMessageBox.warning(self, "Error", 'Please enter all fields')

        elif self.receiving_amount_edit.text() == '':
            QMessageBox.warning(self, "Error", 'Please enter receiving amount')

        elif self.body_table.rowCount() > 0:
            for row in range(self.body_table.rowCount()):
                date = self.body_table.item(row, 9).text()

            # Generate the invoice code
            invoice_code = self.invoice_code_combobox.currentText()
            invoice_date = QDate.fromString(date, "yyyy-MM-dd")
            invoice_date_str = invoice_date.toString("dd-MM-yy")
            invoice_count = self.db.query(Quotation).count() + 1
            invoice_count_str = str(invoice_count).zfill(5)
            invoice_file_name = f"{invoice_code}-{invoice_date_str}-{invoice_count_str}"

            for row in range(self.body_table.rowCount()):
                user_id = self.user_id
                customer_name = self.body_table.item(row, 0).text()
                walk_in_customer = self.body_table.item(row, 1).text()
                product_code = self.body_table.item(row, 2).text()
                product_name = self.body_table.item(row, 3).text()
                brand = self.body_table.item(row, 4).text()
                typ = self.body_table.item(row, 5).text()
                quantity = self.body_table.item(row, 6).text()
                sell_price = self.body_table.item(row, 7).text()
                total_price = self.body_table.item(row, 8).text()
                date = self.body_table.item(row, 9).text()
                grand_total = self.grand_total_edit.text()
                discount = self.discount_edit.text()
                receiving_amount = self.receiving_amount_edit.text()
                remaining_amount = self.remaining_amount_edit.text()

                quotation_item = QuotationItem(
                    user_id=user_id,
                    quotation_id=invoice_file_name,
                    product_code=product_code,
                    product_name=product_name,
                    brand=brand,
                    typ=typ,
                    quantity=quantity,
                    sell_price=sell_price,
                    total_price=total_price
                )

                self.db.add(quotation_item)

            if discount == '':
                discount = 0

            quotation = Quotation(
                user_id=user_id,
                invoice_code=invoice_file_name,
                customer_name=customer_name,
                walk_in_customer=walk_in_customer,
                date=date,
                grand_total=grand_total,
                discount=discount,
                receiving_amount=receiving_amount,
                remaining_amount=remaining_amount
            )

            self.db.add(quotation)

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(invoice_file_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(customer_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(walk_in_customer)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(date)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(discount)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(grand_total)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(receiving_amount)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(remaining_amount)))

            # Create the 'invoices' folder if it doesn't exist
            folder_name = "invoices"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            invoice_file = os.path.join(folder_name, f"{invoice_file_name}.pdf")
            # Generate the invoice HTML content
            invoice_html = self.generate_invoice_html()

            # Save the invoice as a PDF file
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(invoice_file)
            printer.setOrientation(QPrinter.Portrait)

            document = QTextDocument()
            document.setHtml(invoice_html)
            document.print_(printer)

            QMessageBox.information(self, "Success", "Invoice created and saved to the database.")
            self.db.commit()
            self.close()

    def print_invoice(self):
        invoice_html = self.generate_invoice_html()
        folder_name = "invoices"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Generate the file name
        invoice_code = self.invoice_code_combobox.currentText()
        file_name = f"{invoice_code}.pdf"

        # Create the printer object
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOrientation(QPrinter.Portrait)

        # Set the output file path
        output_file = os.path.join(folder_name, file_name)
        printer.setOutputFileName(output_file)

        # Create a print dialog and set the printer
        print_dialog = QPrintDialog(printer)
        print_dialog.setWindowTitle("Print Invoice")

        # If the print dialog is accepted by the user, proceed with printing
        if print_dialog.exec_() == QPrintDialog.Accepted:
            document = QTextDocument()
            document.setHtml(invoice_html)

            # Print the document to the selected printer
            document.print_(printer)

    def generate_invoice_html(self):
        invoice_code = self.invoice_code_combobox.currentText()
        customer_name = self.customer_name_combobox.currentText()
        walk_in_customer = self.walk_in_customer_combobox.text()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        grand_total = self.grand_total_edit.text()
        discount = self.discount_edit.text()
        receiving_amount = self.receiving_amount_edit.text()
        remaining_amount = self.remaining_amount_edit.text()

        items_html = self.generate_items_html()
        invoice_html = f'''
        <html>
            <head>
                <style>
                    /* Define the CSS styles for the invoice */
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .invoice-header {{
                        margin-bottom: 20px;
                    }}
                    .invoice-header h1 {{
                        margin: 0;
                    }}
                    .invoice-info {{
                        margin-bottom: 10px;
                    }}
                    .invoice-info span {{
                        font-weight: bold;
                    }}
                    .invoice-items-table {{
                        margin-bottom: 20px;
                    }}
                    .invoice-total {{
                        text-align: right;
                        margin-bottom: 20px;
                    }}
                    .invoice-total span {{
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="invoice-header">
                    <h1>Sunrays Solar</h1>
                </div>
                <div class="invoice-info">
                    <span>Invoice Code:</span> {invoice_code}<br>
                    <span>Customer Name:</span> {customer_name}<br>
                    <span>Walk-in Customer:</span> {walk_in_customer}<br>
                    <span>Date:</span> {date}<br>
                </div>
                <table class="invoice-items-table">
                    <tr>
                        <th>Product Code</th>
                        <th>Brand</th>
                        <th>Type</th>
                        <th>Quantity</th>
                        <th>Sell Price</th>
                        <th>Total Price</th>
                        <th>Date</th>
                    </tr>
                    {items_html}
                </table>
                <div class="invoice-total">
                    <span>Grand Total:</span> {grand_total}<br>
                    <span>Discount:</span> {discount}<span>%</span><br>
                    <span>Receiving Amount:</span> {receiving_amount}<br>
                    <span>Remaining Amount:</span> {remaining_amount}<br>
                </div>
            </body>
        </html>
        '''

        return invoice_html

    def generate_items_html(self):
        items_html = ''
        for row in range(self.body_table.rowCount()):
            product_code = self.body_table.item(row, 2).text()
            brand = self.body_table.item(row, 4).text()
            typ = self.body_table.item(row, 5).text()
            quantity = self.body_table.item(row, 6).text()
            sell_price = self.body_table.item(row, 7).text()
            total_price = self.body_table.item(row, 8).text()
            date = self.body_table.item(row, 9).text()

            item_html = f'''
            <tr>
                <td>{product_code}</td>
                <td>{brand}</td>
                <td>{typ}</td>
                <td>{quantity}</td>
                <td>{sell_price}</td>
                <td>{total_price}</td>
                <td>{date}</td>
            </tr>
            '''
            items_html += item_html

        return items_html


class AddLaborPaidDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Employee Salary System")
        self.setMinimumSize(1050, 600)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.cnic_label = QLabel("Employee CNIC:")
        self.cnic_edit = QLineEdit()
        self.cnic_edit.textChanged.connect(self.populate_salary_combobox)

        self.labor_name_label = QLabel("Employee Name:")
        self.labor_name_combobox = QLineEdit()

        self.absent_days_label = QLabel("Absent Days:")
        self.absent_days_edit = QLineEdit()

        self.present_days_label = QLabel("Present Days:")
        self.present_days_edit = QLineEdit()
        self.present_days_edit.textChanged.connect(self.populate_remaining_salary_combobox)

        self.salary_label = QLabel("Total Salary:")
        self.salary_edit = QLineEdit()

        self.remaining_salary_label = QLabel("Remaining Salary:")
        self.remaining_salary_edit = QLineEdit()

        self.pay_date_label = QLabel("Pay Date:")
        self.pay_date_edit = QDateEdit(calendarPopup=True)
        self.pay_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.pay_date_edit.setDate(QDate.currentDate())

        header_layout.addWidget(self.cnic_label, 0, 0)
        header_layout.addWidget(self.cnic_edit, 0, 1)
        header_layout.addWidget(self.labor_name_label, 0, 2)
        header_layout.addWidget(self.labor_name_combobox, 0, 3)
        header_layout.addWidget(self.absent_days_label, 1, 0)
        header_layout.addWidget(self.absent_days_edit, 1, 1)
        header_layout.addWidget(self.present_days_label, 1, 2)
        header_layout.addWidget(self.present_days_edit, 1, 3)
        header_layout.addWidget(self.salary_label, 2, 0)
        header_layout.addWidget(self.salary_edit, 2, 1)
        header_layout.addWidget(self.remaining_salary_label, 2, 2)
        header_layout.addWidget(self.remaining_salary_edit, 2, 3)
        header_layout.addWidget(self.pay_date_label, 3, 0)
        header_layout.addWidget(self.pay_date_edit, 3, 1)

        # Create the body section
        headers = ["Employee CNIC", "Employee Name", "Absent Days", "Present Days", "Total Salary", "Remaining Salary",
                   "Pay Date"]
        self.body_table = QTableWidget()
        self.body_table.setColumnCount(len(headers))
        self.body_table.setHorizontalHeaderLabels(headers)
        main_layout.addWidget(self.body_table)
        header = self.body_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the selection behavior to select entire rows
        self.body_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_window)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_from_window)
        self.create_invoice_button = QPushButton("Save")
        self.create_invoice_button.clicked.connect(self.add_salary)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.create_invoice_button)

    def populate_labor_name_combobox(self):
        labor_list = []
        labor_pay = self.db.query(Labor).all()
        if len(labor_pay) >= 1:
            for labor in labor_pay:
                labor_list.append(labor.labor_name)

        self.labor_name_combobox.addItems(labor_list)

    def populate_remaining_salary_combobox(self):
        labor_name = self.labor_name_combobox.text()
        labor_cnic = self.cnic_edit.text()
        present_days = int(self.present_days_edit.text())
        absent_days = int(self.absent_days_edit.text())

        if present_days is None:
            present_days = 0
        if absent_days is None:
            absent_days = 0

        if labor_name and labor_cnic:
            labor = self.db.query(Labor).filter_by(labor_cnic=labor_cnic).first()

            calculate_salary = labor.labor_pay / (present_days + absent_days)
            remaining_salary = calculate_salary * present_days
            if labor:
                self.remaining_salary_edit.setText(str(round(remaining_salary, 2)))
            else:
                self.remaining_salary_edit.setText(str(labor.labor_pay))

    def populate_salary_combobox(self):
        labor_cnic = self.cnic_edit.text()

        if labor_cnic:
            labor = self.db.query(Labor).filter_by(labor_cnic=labor_cnic).first()

            if labor:
                self.salary_edit.setText(str(labor.labor_pay))
                self.labor_name_combobox.setText(str(labor.labor_name))
            else:
                self.salary_edit.setText(str(0))

    def add_to_window(self):
        labor_cnic = self.cnic_edit.text()
        labor_name = self.labor_name_combobox.text()
        absent_days = self.absent_days_edit.text()
        present_days = self.present_days_edit.text()
        labor_pay = self.salary_edit.text()
        remaining_pay = self.remaining_salary_edit.text()
        last_paid = self.pay_date_edit.date().toString("yyyy-MM-dd")

        row_count = self.body_table.rowCount()
        self.body_table.insertRow(row_count)
        self.body_table.setItem(row_count, 0, QTableWidgetItem(labor_cnic))
        self.body_table.setItem(row_count, 1, QTableWidgetItem(labor_name))
        self.body_table.setItem(row_count, 2, QTableWidgetItem(absent_days))
        self.body_table.setItem(row_count, 3, QTableWidgetItem(present_days))
        self.body_table.setItem(row_count, 4, QTableWidgetItem(labor_pay))
        self.body_table.setItem(row_count, 5, QTableWidgetItem(remaining_pay))
        self.body_table.setItem(row_count, 6, QTableWidgetItem(last_paid))

    def delete_from_window(self):
        selected_rows = set()
        labor_name = ''
        labor_cnic = ''

        for item in self.body_table.selectedItems():
            selected_rows.add(item.row())
            labor_cnic = self.body_table.item(item.row(), 1).text()
            labor_name = self.body_table.item(item.row(), 2).text()

        for row in sorted(selected_rows, reverse=True):
            self.body_table.removeRow(row)

    def add_salary(self):
        if self.labor_name_combobox.text() and self.cnic_edit.text() and self.salary_edit.text():
            for row in range(self.body_table.rowCount()):
                user_id = self.user_id
                labor_cnic = self.body_table.item(row, 0).text()
                labor_name = self.body_table.item(row, 1).text()
                absent_days = self.body_table.item(row, 2).text()
                present_days = self.body_table.item(row, 3).text()
                labor_pay = self.body_table.item(row, 4).text()
                remaining_pay = self.body_table.item(row, 5).text()
                last_paid = self.body_table.item(row, 6).text()

                db_labor = self.db.query(Labor).filter_by(labor_name=labor_name, labor_cnic=labor_cnic).first()

                add_salary = LaborPaid(
                    user_id=user_id,
                    labor_id=db_labor.id,
                    labor_name=labor_name,
                    labor_cnic=labor_cnic,
                    absent_days=absent_days,
                    present_days=present_days,
                    remaining_pay=remaining_pay,
                    last_paid=last_paid
                )

                self.db.add(add_salary)

            # Generate the invoice code
            labor_name = self.labor_name_combobox.text()
            salary_date = QDate.fromString(last_paid, "yyyy-MM-dd")
            salary_date_str = salary_date.toString("dd-MM-yy")
            salary_count = self.db.query(LaborPaid).count() + 1
            salary_count_str = str(salary_count).zfill(3)
            salary_file_name = f"{labor_name}-{salary_date_str}-{salary_count_str}"

            folder_name = "salary"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Set the document name
            invoice_file = os.path.join(folder_name, f"{salary_file_name}.pdf")

            # Generate the invoice HTML content
            invoice_html = self.generate_invoice_html()

            # Save the invoice as a PDF file
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(invoice_file)
            printer.setOrientation(QPrinter.Portrait)

            document = QTextDocument()
            document.setHtml(invoice_html)
            document.print_(printer)

            QMessageBox.information(self, "Success", "Salary added Successfully.")
            self.db.commit()
            self.close()
        elif not (
                self.labor_name_combobox.text() and self.cnic_edit.text() and self.salary_edit.text()):
            QMessageBox.warning(self, "Error", 'Please enter all fields')

    def generate_invoice_html(self):
        labor_name = self.labor_name_combobox.text()
        labor_cnic = self.cnic_edit.text()
        labor_pay = self.salary_edit.text()
        remaining_pay = self.remaining_salary_edit.text()
        last_paid = self.pay_date_edit.date().toString("yyyy-MM-dd")

        # Generate the table HTML for invoice items
        items_html = self.generate_items_html()

        # Generate the invoice HTML content
        invoice_html = f'''
        <html>
            <head>
                <style>
                    /* Define the CSS styles for the invoice */
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .invoice-header {{
                        margin-bottom: 20px;
                    }}
                    .invoice-header h1 {{
                        margin: 0;
                    }}
                    .invoice-info {{
                        margin-bottom: 10px;
                    }}
                    .invoice-info span {{
                        font-weight: bold;
                    }}
                    .invoice-items-table {{
                        margin-bottom: 20px;
                    }}
                    .invoice-total {{
                        text-align: right;
                        margin-bottom: 20px;
                    }}
                    .invoice-total span {{
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="invoice-header">
                    <h1>Sunrays Solar</h1>
                </div>
                <div class="invoice-info">
                    <span>Employee Name:</span> {labor_name}<br>
                    <span>CNIC:</span> {labor_cnic}<br>
                    <span>Date:</span> {last_paid}<br>
                </div>
                <table class="invoice-items-table">
                    <tr>
                        <th>Cnic</th>
                        <th>Employee Name</th>
                        <th>Absent Days</th>
                        <th>Present Days</th>
                        <th>Total Salary</th>
                        <th>Remaining Salary</th>
                        <th>Date</th>
                    </tr>
                    {items_html}
                </table>
                <div class="invoice-total">
                    <span>Total Salary:</span> {labor_pay}<br>
                    <span>Remaining Salary:</span> {remaining_pay}<br>
                </div>
            </body>
        </html>
        '''

        return invoice_html

    def generate_items_html(self):
        items_html = ''
        for row in range(self.body_table.rowCount()):
            labor_cnic = self.body_table.item(row, 0).text()
            labor_name = self.body_table.item(row, 1).text()
            absent_days = self.body_table.item(row, 2).text()
            present_days = self.body_table.item(row, 3).text()
            labor_pay = self.body_table.item(row, 4).text()
            remaining_pay = self.body_table.item(row, 5).text()
            last_paid = self.body_table.item(row, 6).text()

            item_html = f'''
            <tr>
                <td>{labor_cnic}</td>
                <td>{labor_name}</td>
                <td>{absent_days}</td>
                <td>{present_days}</td>
                <td>{labor_pay}</td>
                <td>{remaining_pay}</td>
                <td>{last_paid}</td>
            </tr>
            '''
            items_html += item_html

        return items_html


class AddExpanseDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Expanse")
        self.setMinimumSize(800, 500)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.start_label = QLabel("Start:")
        self.start_edit = QDateEdit(calendarPopup=True)
        self.start_edit.setDisplayFormat("dd-MM-yyyy")
        self.start_edit.setDate(QDate.currentDate())

        self.end_label = QLabel("End:")
        self.end_edit = QDateEdit(calendarPopup=True)
        self.end_edit.setDisplayFormat("dd-MM-yyyy")
        self.end_edit.setDate(QDate.currentDate())

        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()

        self.amount_label = QLabel("Amount:")
        self.amount_edit = QLineEdit()
        self.amount_edit.textChanged.connect(self.populate_total_amount_combobox)

        self.date_label = QLabel("Pay Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())

        self.total_label = QLabel("Total Amount:")
        self.total_edit = QLineEdit()

        header_layout.addWidget(self.start_label, 0, 0)
        header_layout.addWidget(self.start_edit, 0, 1)
        header_layout.addWidget(self.end_label, 0, 2)
        header_layout.addWidget(self.end_edit, 0, 3)
        header_layout.addWidget(self.description_label, 1, 0)
        header_layout.addWidget(self.description_edit, 1, 1)
        header_layout.addWidget(self.amount_label, 1, 2)
        header_layout.addWidget(self.amount_edit, 1, 3)
        header_layout.addWidget(self.date_label, 2, 0)
        header_layout.addWidget(self.date_edit, 2, 1)
        header_layout.addWidget(self.total_label, 2, 2)
        header_layout.addWidget(self.total_edit, 2, 3)

        # Create the body section
        headers = ["Description", "amount", "Date"]
        self.body_table = QTableWidget()
        self.body_table.setColumnCount(len(headers))
        self.body_table.setHorizontalHeaderLabels(headers)
        main_layout.addWidget(self.body_table)
        header = self.body_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the selection behavior to select entire rows
        self.body_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.clicked.connect(self.show_data_from_database)
        header_layout.addWidget(self.show_data_button, 1, 4)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_fields)
        header_layout.addWidget(self.clear_button, 2, 4)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_window)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_from_window)
        self.expanse_button = QPushButton("Save")
        self.expanse_button.clicked.connect(self.add_expanse)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.expanse_button)

    def clear_fields(self):
        self.start_edit.clear()
        self.end_edit.clear()
        self.description_edit.clear()
        self.amount_edit.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.total_edit.clear()
        self.body_table.setRowCount(0)

        self.enable_buttons()

    def query_data_from_database(self):
        start_date = self.start_edit.text()
        end_date = self.end_edit.text()
        data = self.db.query(Expanse)

        if start_date and end_date:
            data = data.filter(and_(Expanse.date >= start_date, Expanse.date <= end_date))
        return data.all()

    def show_data_from_database(self):
        if self.start_edit.text() and self.end_edit.text():
            data = self.query_data_from_database()
            self.update_table_with_data(data)

            # Disable the buttons after showing the data
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.expanse_button.setEnabled(False)

        if not (self.start_edit.text() and self.end_edit.text()):
            QMessageBox.warning(self, "Error", 'Please Enter Start and End date')

    def update_table_with_data(self, data):
        self.body_table.setRowCount(0)
        for row_num, expanse in enumerate(data, 0):
            description = expanse.description
            amount = str(expanse.amount)
            date = expanse.date

            self.body_table.insertRow(row_num)
            self.body_table.setItem(row_num, 0, QTableWidgetItem(description))
            self.body_table.setItem(row_num, 1, QTableWidgetItem(amount))
            self.body_table.setItem(row_num, 2, QTableWidgetItem(date))

        self.populate_total_amount_combobox()

    def add_to_window(self):
        description = self.description_edit.text()
        amount = self.amount_edit.text()
        date = self.date_edit.date().toString("dd-MM-yyyy")

        row_count = self.body_table.rowCount()
        self.body_table.insertRow(row_count)
        self.body_table.setItem(row_count, 0, QTableWidgetItem(description))
        self.body_table.setItem(row_count, 1, QTableWidgetItem(amount))
        self.body_table.setItem(row_count, 2, QTableWidgetItem(date))

        self.populate_total_amount_combobox()

    def delete_from_window(self):
        selected_rows = set()

        for item in self.body_table.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            total_price_item = self.body_table.item(row, 1)
            if total_price_item:
                total_price = float(total_price_item.text())
                self.total_edit.setText(str(float(self.total_edit.text()) - total_price))
            self.body_table.removeRow(row)

        self.populate_total_amount_combobox()

    def populate_total_amount_combobox(self):
        total_amount = 0
        for row in range(self.body_table.rowCount()):
            total_price_item = self.body_table.item(row, 1)
            if total_price_item:
                total_price = float(total_price_item.text())
                total_amount += total_price

        self.total_edit.setText(str(total_amount))

    def enable_buttons(self):
        self.add_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.expanse_button.setEnabled(True)

    def add_expanse(self):
        if self.description_edit.text() and self.amount_edit.text():
            for row in range(self.body_table.rowCount()):
                user_id = self.user_id
                description = self.body_table.item(row, 0).text()
                amount = self.body_table.item(row, 1).text()
                date = self.body_table.item(row, 2).text()

                add_expanse = Expanse(
                    user_id=user_id,
                    description=description,
                    amount=amount,
                    date=date,
                )

                self.db.add(add_expanse)

            QMessageBox.information(self, "Success", "Expanse added Successfully.")

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(description)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(amount)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(date)))

            self.db.commit()
            self.close()

        elif not (self.description_edit.text() and self.amount_edit.text()):
            QMessageBox.warning(self, "Error", 'Please enter all fields')


class AddProjectDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Project")
        self.setMinimumSize(800, 250)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.start_label = QLabel("Search To:")
        self.start_edit = QDateEdit(calendarPopup=True)
        self.start_edit.setDisplayFormat("dd-MM-yyyy")
        self.start_edit.setDate(QDate.currentDate())

        self.end_label = QLabel("From:")
        self.end_edit = QDateEdit(calendarPopup=True)
        self.end_edit.setDisplayFormat("dd-MM-yyyy")
        self.end_edit.setDate(QDate.currentDate())

        self.project_code_label = QLabel("Project Code:")
        self.project_code_edit = QLineEdit()

        self.project_name_label = QLabel("Project Name:")
        self.project_name_edit = QLineEdit()

        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_edit = QLineEdit()

        self.project_cost_label = QLabel("Project Cost:")
        self.project_cost_edit = QLineEdit()

        self.receiving_amount_label = QLabel("Receiving Amount:")
        self.receiving_amount_edit = QLineEdit()
        self.receiving_amount_edit.textChanged.connect(self.update_remaining_amount)

        self.remaining_amount_label = QLabel("Remaining Amount:")
        self.remaining_amount_edit = QLineEdit()

        self.date_label = QLabel("start Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())

        header_layout.addWidget(self.start_label, 0, 0)
        header_layout.addWidget(self.start_edit, 0, 1)
        header_layout.addWidget(self.end_label, 0, 2)
        header_layout.addWidget(self.end_edit, 0, 3)
        header_layout.addWidget(self.project_code_label, 1, 0)
        header_layout.addWidget(self.project_code_edit, 1, 1)
        header_layout.addWidget(self.project_name_label, 1, 2)
        header_layout.addWidget(self.project_name_edit, 1, 3)
        header_layout.addWidget(self.address_label, 2, 0)
        header_layout.addWidget(self.address_edit, 2, 1)
        header_layout.addWidget(self.description_label, 2, 2)
        header_layout.addWidget(self.description_edit, 2, 3)
        header_layout.addWidget(self.project_cost_label, 3, 0)
        header_layout.addWidget(self.project_cost_edit, 3, 1)
        header_layout.addWidget(self.receiving_amount_label, 3, 2)
        header_layout.addWidget(self.receiving_amount_edit, 3, 3)
        header_layout.addWidget(self.remaining_amount_label, 3, 4)
        header_layout.addWidget(self.remaining_amount_edit, 3, 5)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_project)

        button_layout.addWidget(self.save_button)

    def update_remaining_amount(self):
        project_cost = self.project_cost_edit.text()
        receiving_amount = self.receiving_amount_edit.text()

        if project_cost and receiving_amount:
            remaining_amount = int(project_cost) - int(receiving_amount)
            self.remaining_amount_edit.setText(str(remaining_amount))
        else:
            self.remaining_amount_edit.clear()

    def add_project(self):
        if self.project_cost_edit.text() and self.receiving_amount_edit.text() and self.remaining_amount_edit.text():
            db_code = self.db.query(Projects).filter_by(project_code=self.project_code_edit.text()).first()
            if db_code is None:
                user_id = self.user_id
                project_code = self.project_code_edit.text()
                project_name = self.project_name_edit.text()
                description = self.description_edit.text()
                address = self.address_edit.text()
                project_cost = self.project_cost_edit.text()
                receiving_amount = self.receiving_amount_edit.text()
                remaining_amount = self.remaining_amount_edit.text()
                date = self.date_edit.text()

                add_project = Projects(
                    user_id=user_id,
                    project_code=project_code,
                    project_name=project_name,
                    description=description,
                    address=address,
                    project_cost=project_cost,
                    receiving_amount=receiving_amount,
                    remaining_amount=remaining_amount,
                    date=date,
                )

                self.db.add(add_project)

                QMessageBox.information(self, "Success", "Project added Successfully.")
                self.db.commit()
                self.close()

            else:
                QMessageBox.warning(self, "Error", 'This Project code Already exist')

        elif not (self.description_edit.text() and self.amount_edit.text()):
            QMessageBox.warning(self, "Error", 'Please enter all fields')


class AddPanelDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Panel")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.capacity_label = QLabel("Capacity:")
        self.capacity_input = QLineEdit()
        self.layout.addWidget(self.capacity_label)
        self.layout.addWidget(self.capacity_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_panel)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['Panel']
        self.product_name_combobox.addItems(product_list)

    def add_panel(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.capacity_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.capacity_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            capacity = self.capacity_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Panel(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                capacity=capacity,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(capacity)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(sell_price)))

            self.close()


class AddInverterDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Inverter")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.power_rating_label = QLabel("Power Rating:")
        self.power_rating_input = QLineEdit()
        self.layout.addWidget(self.power_rating_label)
        self.layout.addWidget(self.power_rating_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_inverter)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['Inverter']
        self.product_name_combobox.addItems(product_list)

    def add_inverter(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.power_rating_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.power_rating_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            power_rating = self.power_rating_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Inverter(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                power_rating=power_rating,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(power_rating)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(sell_price)))

            self.close()


class AddFrameDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Frame")
        self.setMinimumSize(300, 500)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.width_label = QLabel("Width:")
        self.width_input = QLineEdit()
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)

        self.height_label = QLabel("Height:")
        self.height_input = QLineEdit()
        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_frame)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['Frame']
        self.product_name_combobox.addItems(product_list)

    def add_frame(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.width_input.text() and self.height_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.width_input.text() and self.height_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            width = self.width_input.text()
            height = self.height_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Frame(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                width=width,
                height=height,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(width)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(height)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 9, QTableWidgetItem(str(sell_price)))

            self.close()


class AddACCableDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add AC-Cable")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.size_label = QLabel("Size:")
        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_cable)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['ACCable']
        self.product_name_combobox.addItems(product_list)

    def add_cable(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            size = self.size_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = ACCable(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                size=size,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(size)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(sell_price)))

            self.close()


class AddDCCableDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add DC-Cable")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.size_label = QLabel("Size:")
        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_cable)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['DCCable']
        self.product_name_combobox.addItems(product_list)

    def add_cable(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.size_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            size = self.size_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = DCCable(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                size=size,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(size)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(sell_price)))

            self.close()


class AddBatteryDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Battery")
        self.setMinimumSize(300, 600)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.warranty_label = QLabel("Warranty:")
        self.warranty_input = QLineEdit()
        self.layout.addWidget(self.warranty_label)
        self.layout.addWidget(self.warranty_input)

        self.capacity_label = QLabel("Capacity:")
        self.capacity_input = QLineEdit()
        self.layout.addWidget(self.capacity_label)
        self.layout.addWidget(self.capacity_input)

        self.voltage_label = QLabel("Voltage:")
        self.voltage_input = QLineEdit()
        self.layout.addWidget(self.voltage_label)
        self.layout.addWidget(self.voltage_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_battery)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['Battery']
        self.product_name_combobox.addItems(product_list)

    def add_battery(self):
        if not (
                self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.warranty_input.text() and self.capacity_input.text() and self.voltage_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.brand_input.text() and self.type_input.text() and self.warranty_input.text() and self.capacity_input.text() and self.voltage_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            warranty = self.warranty_input.text()
            capacity = self.capacity_input.text()
            voltage = self.voltage_input.text()
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 1
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''

            panel = Battery(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                warranty=warranty,
                capacity=capacity,
                voltage=voltage,
                quantity=quantity,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_code)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(warranty)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(capacity)))
            self.table_widget.setItem(row_count, 7, QTableWidgetItem(str(voltage)))
            self.table_widget.setItem(row_count, 8, QTableWidgetItem(str(quantity)))
            self.table_widget.setItem(row_count, 9, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 10, QTableWidgetItem(str(sell_price)))

            self.close()


class AddAccessoriesDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Accessories")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.product_code_label = QLabel("Product Code:")
        self.product_code_input = QLineEdit()
        self.layout.addWidget(self.product_code_label)
        self.layout.addWidget(self.product_code_input)

        self.product_name_label = QLabel("Product Name:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.purchase_price_label = QLabel("Purchase Price:")
        self.purchase_price_input = QLineEdit()
        self.layout.addWidget(self.purchase_price_label)
        self.layout.addWidget(self.purchase_price_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_customer)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def populate_product_name_combobox(self):
        product_list = ['Accessories']
        self.product_name_combobox.addItems(product_list)

    def add_customer(self):
        if not (
                self.product_name_input.text() and self.type_input.text() and self.brand_input.text() and self.purchase_price_input.text() and self.sell_price_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.product_name_input.text() and self.type_input.text() and self.brand_input.text() and self.purchase_price_input.text() and self.sell_price_input.text():
            user_id = self.user_id
            product_code = self.product_code_input.text()
            product_name = self.product_name_input.text()
            brand = self.brand_input.text()
            typ = self.type_input.text()
            purchase_price = float(self.purchase_price_input.text()) if self.purchase_price_input.text() else ''
            sell_price = float(self.sell_price_input.text()) if self.sell_price_label.text() else ''

            panel = Accessories(
                user_id=user_id,
                product_code=product_code,
                product_name=product_name,
                brand=brand,
                typ=typ,
                purchase_price=purchase_price,
                sell_price=sell_price
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(purchase_price)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(sell_price)))

            self.close()


class AddLaborDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Employee")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.labor_name_label = QLabel("Employee Name:")
        self.labor_name_input = QLineEdit()
        self.layout.addWidget(self.labor_name_label)
        self.layout.addWidget(self.labor_name_input)

        self.date_label = QLabel("Start Date:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_edit)

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()
        self.layout.addWidget(self.phone_number_label)
        self.layout.addWidget(self.phone_number_input)

        self.labor_cnic_label = QLabel("Employee CNIC:")
        self.labor_cnic_input = QLineEdit()
        self.layout.addWidget(self.labor_cnic_label)
        self.layout.addWidget(self.labor_cnic_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.pay_label = QLabel("Salary:")
        self.pay_input = QLineEdit()
        self.layout.addWidget(self.pay_label)
        self.layout.addWidget(self.pay_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_labor)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def add_labor(self):
        if not (
                self.labor_name_input.text() and self.date_edit.text() and self.phone_number_input.text() and self.labor_cnic_input.text() and self.address_input.text() and self.pay_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.labor_name_input.text() and self.date_edit.text() and self.phone_number_input.text() and self.labor_cnic_input.text() and self.address_input.text() and self.pay_input.text():
            user_id = self.user_id
            labor_name = self.labor_name_input.text()
            start_date = self.date_edit.date().toString("dd-MM-yyyy")
            phone_number = self.phone_number_input.text()
            labor_cnic = self.labor_cnic_input.text()
            labor_address = self.address_input.text()
            labor_pay = int(self.pay_input.text()) if self.pay_input.text() else 0

            panel = Labor(
                user_id=user_id,
                labor_name=labor_name,
                start_date=start_date,
                phon_number=phone_number,
                labor_cnic=labor_cnic,
                labor_address=labor_address,
                labor_pay=labor_pay,
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            # self.table_widget.setItem(row_count, 1, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(labor_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(start_date)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(phone_number)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(labor_cnic)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(labor_address)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(labor_pay)))

            self.close()


class AddSupplierDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Supplier")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.supplier_name_label = QLabel("Supplier Name:")
        self.supplier_name_input = QLineEdit()
        self.layout.addWidget(self.supplier_name_label)
        self.layout.addWidget(self.supplier_name_input)

        self.company_label = QLabel("Company:")
        self.company_input = QLineEdit()
        self.layout.addWidget(self.company_label)
        self.layout.addWidget(self.company_input)

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()
        self.layout.addWidget(self.phone_number_label)
        self.layout.addWidget(self.phone_number_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_labor)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def add_labor(self):
        if not (
                self.supplier_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.address_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.supplier_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.address_input.text():
            user_id = self.user_id
            supplier_name = self.supplier_name_input.text()
            company = self.company_input.text()
            phone_number = self.phone_number_input.text()
            email = self.email_input.text()
            address = self.address_input.text()

            panel = Supplier(
                user_id=user_id,
                supplier_name=supplier_name,
                company=company,
                phon_number=phone_number,
                email=email,
                address=address
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            # self.table_widget.setItem(row_count, 1, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(supplier_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(company)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(phone_number)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(email)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(address)))

            self.close()


class AddCustomerDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Customer")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_input = QLineEdit()
        self.layout.addWidget(self.customer_name_label)
        self.layout.addWidget(self.customer_name_input)

        self.company_label = QLabel("Company:")
        self.company_input = QLineEdit()
        self.layout.addWidget(self.company_label)
        self.layout.addWidget(self.company_input)

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()
        self.layout.addWidget(self.phone_number_label)
        self.layout.addWidget(self.phone_number_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()
        self.layout.addWidget(self.city_label)
        self.layout.addWidget(self.city_input)

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_labor)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

    def add_labor(self):
        if not (
                self.customer_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.city_input.text() and self.address_input.text()):
            QMessageBox.warning(self, "Error", "All fields are required.")

        if self.customer_name_input.text() and self.company_input.text() and self.phone_number_input.text() and self.email_input.text() and self.city_input.text() and self.address_input.text():
            user_id = self.user_id
            customer_name = self.customer_name_input.text()
            company = self.company_input.text()
            phone_number = self.phone_number_input.text()
            email = self.email_input.text()
            city = self.city_input.text()
            address = self.address_input.text()

            panel = Customer(
                user_id=user_id,
                customer_name=customer_name,
                company=company,
                phone_number=phone_number,
                email=email,
                city=city,
                address=address
            )
            self.db.add(panel)
            self.db.commit()

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            # self.table_widget.setItem(row_count, 1, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(customer_name)))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(company)))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(phone_number)))
            self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(email)))
            self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(city)))
            self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(address)))

            self.close()


class AddQuotationItemDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Quotation Item")
        self.setMinimumSize(300, 400)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.quotation_id_label = QLabel("Quotation Id:")
        self.quotation_id_input = QLineEdit()
        self.layout.addWidget(self.quotation_id_label)
        self.layout.addWidget(self.quotation_id_input)

        # self.product_name_label = QLabel("Product Name:")
        # self.product_name_input = QComboBox()
        # self.layout.addWidget(self.product_name_label)
        # self.layout.addWidget(self.product_name_input)

        self.product_name_label = QLabel("Brand:")
        self.product_name_input = QLineEdit()
        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_name_input)

        self.brand_label = QLabel("Brand:")
        self.brand_input = QLineEdit()
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_input)

        self.type_label = QLabel("Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        self.sell_price_label = QLabel("Sell Price:")
        self.sell_price_input = QLineEdit()
        self.layout.addWidget(self.sell_price_label)
        self.layout.addWidget(self.sell_price_input)

        self.total_price_label = QLabel("Total Price:")
        self.total_price_input = QLineEdit()
        self.layout.addWidget(self.total_price_label)
        self.layout.addWidget(self.total_price_input)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_quotation_item)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

        # Populate the item input with data from the database
        self.populate_item_input()

    def populate_item_input(self):
        items_list = [
            (Panel, 'product_name'),
            (Inverter, 'product_name'),
            (Frame, 'product_name'),
            (ACCable, 'product_name'),
            (DCCable, 'product_name'),
            (Battery, 'product_name'),
            (Accessories, 'product_name')
        ]

        # Clear the current items in the combobox
        self.item_input.clear()

        # Add the items to the combobox
        for item_type, attribute_name in items_list:
            items = self.db.query(item_type).all()
            for item in items:
                item_name = getattr(item, attribute_name)
                self.item_input.addItem(item_name)

    def add_quotation_item(self):
        user_id = self.user_id
        quotation_id = self.quotation_id_input.text()
        product_name = self.product_name_input.text()
        brand = self.brand_input.text()
        typ = self.type_input.text()
        quantity = int(self.quantity_input.text()) if self.quantity_input.text() else ''
        sell_price = float(self.sell_price_input.text()) if self.sell_price_input.text() else ''
        total_price = float(self.total_price_input.text()) if self.total_price_input.text() else ''

        quotation_item = QuotationItem(
            user_id=user_id,
            quotation_id=quotation_id,
            product_name=product_name,
            brand=brand,
            typ=typ,
            quantity=quantity,
            sell_price=sell_price,
            total_price=total_price
        )
        self.db.add(quotation_item)
        self.db.commit()

        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(product_name)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(brand)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(typ)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(quantity)))
        self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(sell_price)))
        self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(total_price)))

        self.close()


class BanksPaymentsDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Payment")
        self.setMinimumSize(500, 200)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.user_name_label = QLabel("User Name:")
        self.user_name_edit = QLineEdit()

        self.account_number_label = QLabel("Account No:")
        self.account_number_edit = QLineEdit()
        self.account_number_edit.textChanged.connect(self.show_amount)

        self.bank_name_label = QLabel("Bank Name:")
        self.bank_name_edit = QComboBox()
        self.bank_name_list()

        self.amount_label = QLabel("Amount:")
        self.amount_edit = QLineEdit()
        self.amount_edit.textChanged.connect(self.populate_total_amount_combobox)

        self.adding_date_label = QLabel("Date:")
        self.adding_date_edit = QDateEdit(calendarPopup=True)
        self.adding_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.adding_date_edit.setDate(QDate.currentDate())

        self.total_label = QLabel("Total Amount:")
        self.total_edit = QLineEdit()

        header_layout.addWidget(self.bank_name_label, 0, 0)
        header_layout.addWidget(self.bank_name_edit, 0, 1)
        header_layout.addWidget(self.account_number_label, 0, 2)
        header_layout.addWidget(self.account_number_edit, 0, 3)
        header_layout.addWidget(self.user_name_label, 1, 0)
        header_layout.addWidget(self.user_name_edit, 1, 1)
        header_layout.addWidget(self.amount_label, 1, 2)
        header_layout.addWidget(self.amount_edit, 1, 3)
        header_layout.addWidget(self.adding_date_label, 2, 0)
        header_layout.addWidget(self.adding_date_edit, 2, 1)
        header_layout.addWidget(self.total_label, 2, 2)
        header_layout.addWidget(self.total_edit, 2, 3)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_bank)

        button_layout.addWidget(self.save_button)

    def bank_name_list(self):
        bank_list = ['National Bank of Pakistan', 'United Bank Limited', 'MCB Bank Limited', 'Allied Bank Limited',
                     'Faysal Bank Limited', 'Bank Al Habib Limited', 'Askari Bank Limited',
                     'BankIslami Pakistan Limited']
        self.bank_name_edit.addItems(bank_list)

    def show_amount(self):
        account_number = self.account_number_edit.text()
        bank_data = self.db.query(Banks).filter_by(account_number=account_number).first()
        if bank_data is not None:
            self.total_edit.setText(str(bank_data.amount))
            self.user_name_edit.setText(str(bank_data.user_name))

    def populate_total_amount_combobox(self):
        total_price = self.amount_edit.text()
        account_number = self.account_number_edit.text()
        data = self.db.query(Banks).filter_by(account_number=account_number).first()

        if data is not None:
            total_amount = float(data.amount) + float(total_price)
            self.total_edit.setText(str(total_amount))

    def add_bank(self):
        account_number = self.account_number_edit.text()
        get_account = self.db.query(Banks).filter_by(account_number=account_number).first()
        if get_account is None:
            if self.bank_name_edit.currentText() and self.user_name_edit and self.account_number_edit and self.amount_edit.text():
                add_bank = Banks(
                    user_id=self.user_id,
                    user_name=self.user_name_edit.text(),
                    account_number=self.account_number_edit.text(),
                    bank_name=self.bank_name_edit.currentText(),
                    amount=self.amount_edit.text(),
                    transaction_date=self.adding_date_edit.text(),
                )

                self.db.add(add_bank)

                QMessageBox.information(self, "Success", "Amount added Successfully.")
                self.db.commit()
                self.close()

            elif not (
                    self.bank_name_edit.currentText() and self.user_name_edit and self.account_number_edit and self.amount_edit.text()):
                QMessageBox.warning(self, "Error", 'Please enter all fields')

        elif get_account is not None:
            update_amount = get_account.amount + int(self.amount_edit.text())
            get_account.user_name = self.user_name_edit.text()
            get_account.account_number = self.account_number_edit.text()
            get_account.bank_name = self.bank_name_edit.currentText()
            get_account.amount = float(update_amount)
            get_account.transaction_date = self.adding_date_edit.text()

            QMessageBox.warning(self, "Warning", "Amount added Successfully.")
            self.db.commit()
            self.close()


class BanksTransactionsDialog(QDialog):
    def __init__(self, db, user_id, table_widget):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.table_widget = table_widget
        self.setWindowTitle("Add Transaction")
        self.setMinimumSize(900, 500)
        self.setModal(True)

        # Create the layout for the dialog
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create the header section
        header_layout = QGridLayout()
        main_layout.addLayout(header_layout)

        self.start_label = QLabel("Start:")
        self.start_edit = QDateEdit(calendarPopup=True)
        self.start_edit.setDisplayFormat("dd-MM-yyyy")
        self.start_edit.setDate(QDate.currentDate())

        self.end_label = QLabel("End:")
        self.end_edit = QDateEdit(calendarPopup=True)
        self.end_edit.setDisplayFormat("dd-MM-yyyy")
        self.end_edit.setDate(QDate.currentDate())

        self.account_number_label = QLabel("Account No:")
        self.account_number_edit = QLineEdit()
        self.account_number_edit.textChanged.connect(self.get_db_data)

        self.bank_name_label = QLabel("Bank Name:")
        self.bank_name_edit = QLineEdit()
        # self.bank_name_list()

        self.user_name_label = QLabel("User Name:")
        self.user_name_edit = QLineEdit()

        self.amount_label = QLabel("Amount:")
        self.amount_edit = QLineEdit()
        self.amount_edit.textChanged.connect(self.populate_total_amount_combobox)

        self.description_label = QLabel("Description:")
        self.description_edit = QLineEdit()

        self.transaction_date_label = QLabel("Transaction Date:")
        self.transaction_date_edit = QDateEdit(calendarPopup=True)
        self.transaction_date_edit.setDisplayFormat("dd-MM-yyyy")
        self.transaction_date_edit.setDate(QDate.currentDate())

        self.total_label = QLabel("Total Amount:")
        self.total_edit = QLineEdit()

        header_layout.addWidget(self.start_label, 0, 0)
        header_layout.addWidget(self.start_edit, 0, 1)
        header_layout.addWidget(self.end_label, 0, 2)
        header_layout.addWidget(self.end_edit, 0, 3)
        header_layout.addWidget(self.account_number_label, 1, 0)
        header_layout.addWidget(self.account_number_edit, 1, 1)
        header_layout.addWidget(self.bank_name_label, 1, 2)
        header_layout.addWidget(self.bank_name_edit, 1, 3)
        header_layout.addWidget(self.user_name_label, 2, 0)
        header_layout.addWidget(self.user_name_edit, 2, 1)
        header_layout.addWidget(self.amount_label, 2, 2)
        header_layout.addWidget(self.amount_edit, 2, 3)
        header_layout.addWidget(self.description_label, 3, 0)
        header_layout.addWidget(self.description_edit, 3, 1)
        header_layout.addWidget(self.transaction_date_label, 3, 2)
        header_layout.addWidget(self.transaction_date_edit, 3, 3)
        header_layout.addWidget(self.total_label, 4, 0)
        header_layout.addWidget(self.total_edit, 4, 1)

        # Create the body section
        headers = ["User Name", "Account No", "Bank Name", "Amount", "Description", "Date"]
        self.body_table = QTableWidget()
        self.body_table.setColumnCount(len(headers))
        self.body_table.setHorizontalHeaderLabels(headers)
        main_layout.addWidget(self.body_table)
        header = self.body_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the selection behavior to select entire rows
        self.body_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Create the button section
        button_layout = QHBoxLayout()
        button_layout.setMargin(10)
        main_layout.addLayout(button_layout)

        # Add spacer item to push buttons to the right side
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_layout.addWidget(spacer_item)

        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.clicked.connect(self.show_data_from_database)
        header_layout.addWidget(self.show_data_button, 0, 4)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_fields)
        header_layout.addWidget(self.clear_button, 1, 4)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_window)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_from_window)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_bank)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.save_button)

    def clear_fields(self):
        self.user_name_edit.clear()
        self.account_number_edit.clear()
        self.amount_edit.clear()
        self.description_edit.clear()
        self.transaction_date_edit.setDate(QDate.currentDate())
        self.total_edit.clear()
        self.body_table.setRowCount(0)

        self.enable_buttons()

    def get_db_data(self):
        account_number = self.account_number_edit.text()
        db_data = self.db.query(Banks).filter_by(account_number=account_number).first()

        if db_data is not None:
            self.user_name_edit.setText(db_data.user_name)
            self.bank_name_edit.setText(db_data.bank_name)
            self.total_edit.setText(str(db_data.amount))

    def query_data_from_database(self):
        start_date = self.start_edit.text()
        end_date = self.end_edit.text()
        bank_name = self.bank_name_edit.text()
        data = self.db.query(BankTransaction)

        if start_date and end_date:
            data = data.filter(BankTransaction.transaction_date >= start_date,
                               BankTransaction.transaction_date <= end_date,
                               BankTransaction.bank_name == bank_name)

        return data.all()

    def show_data_from_database(self):
        if self.start_edit.text() and self.end_edit.text():
            data = self.query_data_from_database()
            self.update_table_with_data(data)

            # Disable the buttons after showing the data
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.save_button.setEnabled(False)

        if not (self.start_edit.text() and self.end_edit.text()):
            QMessageBox.warning(self, "Error", 'Please Enter Start and End date')

    def update_table_with_data(self, data):
        self.body_table.setRowCount(0)
        for row_num, bank in enumerate(data, 0):
            user_name = bank.user_name
            account_number = bank.account_number
            bank_name = bank.bank_name
            amount = str(bank.amount)
            description = str(bank.description)
            transaction_date = bank.transaction_date

            self.body_table.insertRow(row_num)
            self.body_table.setItem(row_num, 0, QTableWidgetItem(user_name))
            self.body_table.setItem(row_num, 1, QTableWidgetItem(account_number))
            self.body_table.setItem(row_num, 2, QTableWidgetItem(bank_name))
            self.body_table.setItem(row_num, 3, QTableWidgetItem(amount))
            self.body_table.setItem(row_num, 4, QTableWidgetItem(description))
            self.body_table.setItem(row_num, 5, QTableWidgetItem(transaction_date))

        self.populate_total_amount_combobox()

    def add_to_window(self):
        user_name = self.user_name_edit.text()
        account_number = self.account_number_edit.text()
        bank_name = self.bank_name_edit.text()
        amount = self.amount_edit.text()
        description = self.description_edit.text()
        transaction_date = self.transaction_date_edit.date().toString("dd-MM-yyyy")

        row_count = self.body_table.rowCount()
        self.body_table.insertRow(row_count)
        self.body_table.setItem(row_count, 0, QTableWidgetItem(user_name))
        self.body_table.setItem(row_count, 1, QTableWidgetItem(account_number))
        self.body_table.setItem(row_count, 2, QTableWidgetItem(bank_name))
        self.body_table.setItem(row_count, 3, QTableWidgetItem(amount))
        self.body_table.setItem(row_count, 4, QTableWidgetItem(description))
        self.body_table.setItem(row_count, 5, QTableWidgetItem(transaction_date))

        self.populate_total_amount_combobox()

    def delete_from_window(self):
        selected_rows = set()

        for item in self.body_table.selectedItems():
            selected_rows.add(item.row())

        for row in sorted(selected_rows, reverse=True):
            total_price_item = self.body_table.item(row, 3)
            if total_price_item:
                total_price = float(total_price_item.text())
                self.total_edit.setText(str(float(self.total_edit.text()) - total_price))
            self.body_table.removeRow(row)

        self.populate_total_amount_combobox()

    def populate_total_amount_combobox(self):
        total_amount = 0
        for row in range(self.body_table.rowCount()):
            total_price_item = self.body_table.item(row, 3)
            if total_price_item:
                total_price = float(total_price_item.text())
                total_amount += total_price

        self.total_edit.setText(str(total_amount))

    def enable_buttons(self):
        self.add_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def add_bank(self):
        account_number = self.account_number_edit.text()
        get_account = self.db.query(Banks).filter_by(account_number=account_number).first()
        if get_account is not None:
            db_amount = get_account.amount
            total_price = self.total_edit.text()
            if self.bank_name_edit.text() and self.account_number_edit and self.amount_edit.text():
                for row in range(self.body_table.rowCount()):
                    user_id = self.user_id
                    bank_id = get_account.id
                    user_name = self.body_table.item(row, 0).text()
                    account_number = self.body_table.item(row, 1).text()
                    bank_name = self.body_table.item(row, 2).text()
                    amount = self.body_table.item(row, 3).text()
                    description = self.body_table.item(row, 4).text()
                    transaction_date = self.body_table.item(row, 5).text()

                    add_bank = BankTransaction(
                        user_id=user_id,
                        bank_id=bank_id,
                        user_name=user_name,
                        account_number=account_number,
                        bank_name=bank_name,
                        description=description,
                        amount=amount,
                        transaction_date=transaction_date,
                    )

                    self.db.add(add_bank)

                if get_account.amount >= float(total_price):
                    QMessageBox.information(self, "Success", "Transaction Successfully.")
                    get_account.amount = float(db_amount) - float(total_price)
                    self.db.commit()
                    self.close()

                elif not (get_account.amount >= float(total_price)):
                    QMessageBox.warning(self, "Error", 'Insufficient Balance.')

            elif not (self.bank_name_edit.text() and self.account_number_edit and self.amount_edit.text()):
                QMessageBox.warning(self, "Error", 'Please enter all fields')

        elif get_account is None:
            QMessageBox.warning(self, "Error", "Invalid Account.")


class UpdateItemDialog(QDialog):
    def __init__(self, db, todo_stack):
        super().__init__()
        self.db = db
        self.todo_stack = todo_stack
        self.update_item()

    def update_item(self):
        current_index = self.todo_stack.currentIndex()
        todo_widget = self.todo_stack.widget(current_index)
        table_widget = todo_widget.findChild(QTableWidget)
        selected_items = table_widget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Error", "No item selected.")
            return

        # Get the row index of the selected item
        selected_row = selected_items[0].row()

        # Get the item ID from the first column of the selected row
        item = table_widget.item(selected_row, 0)
        item_id = item.text() if item is not None else ""

        if current_index == 1:
            panel = self.db.query(Panel).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if panel:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                capacity = table_widget.item(selected_row, 5).text()
                quantity = table_widget.item(selected_row, 6).text()
                purchase_price = table_widget.item(selected_row, 7).text()
                sell_price = table_widget.item(selected_row, 8).text()

                panel.product_code = product_code
                panel.product_name = product_name
                panel.brand = brand
                panel.typ = typ
                panel.capacity = capacity
                panel.quantity = quantity
                panel.purchase_price = purchase_price
                panel.sell_price = sell_price

                self.db.commit()

        elif current_index == 2:
            inverter = self.db.query(Inverter).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if inverter:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                power_rating = table_widget.item(selected_row, 5).text()
                quantity = table_widget.item(selected_row, 6).text()
                purchase_price = table_widget.item(selected_row, 7).text()
                sell_price = table_widget.item(selected_row, 8).text()

                inverter.product_code = product_code
                inverter.product_name = product_name
                inverter.brand = brand
                inverter.typ = typ
                inverter.power_rating = power_rating
                inverter.quantity = quantity
                inverter.purchase_price = purchase_price
                inverter.sell_price = sell_price

                self.db.commit()

        elif current_index == 3:
            frame = self.db.query(Frame).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if frame:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                width = table_widget.item(selected_row, 5).text()
                height = table_widget.item(selected_row, 6).text()
                quantity = table_widget.item(selected_row, 7).text()
                purchase_price = table_widget.item(selected_row, 8).text()
                sell_price = table_widget.item(selected_row, 9).text()

                frame.product_code = product_code
                frame.product_name = product_name
                frame.brand = brand
                frame.typ = typ
                frame.width = width
                frame.height = height
                frame.quantity = quantity
                frame.purchase_price = purchase_price
                frame.sell_price = sell_price

                self.db.commit()

        elif current_index == 4:
            coil = self.db.query(ACCable).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if coil:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                size = table_widget.item(selected_row, 5).text()
                quantity = table_widget.item(selected_row, 6).text()
                purchase_price = table_widget.item(selected_row, 7).text()
                sell_price = table_widget.item(selected_row, 8).text()

                coil.product_code = product_code
                coil.product_name = product_name
                coil.brand = brand
                coil.typ = typ
                coil.size = size
                coil.quantity = quantity
                coil.purchase_price = purchase_price
                coil.sell_price = sell_price

                self.db.commit()

        elif current_index == 5:
            coil = self.db.query(DCCable).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if coil:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                size = table_widget.item(selected_row, 5).text()
                quantity = table_widget.item(selected_row, 6).text()
                purchase_price = table_widget.item(selected_row, 7).text()
                sell_price = table_widget.item(selected_row, 8).text()

                coil.product_code = product_code
                coil.product_name = product_name
                coil.brand = brand
                coil.typ = typ
                coil.size = size
                coil.quantity = quantity
                coil.purchase_price = purchase_price
                coil.sell_price = sell_price

                self.db.commit()

        elif current_index == 6:
            battery = self.db.query(Battery).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if battery:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                warranty = table_widget.item(selected_row, 5).text()
                capacity = table_widget.item(selected_row, 6).text()
                voltage = table_widget.item(selected_row, 7).text()
                quantity = table_widget.item(selected_row, 8).text()
                purchase_price = table_widget.item(selected_row, 9).text()
                sell_price = table_widget.item(selected_row, 10).text()

                battery.product_code = product_code
                battery.product_name = product_name
                battery.brand = brand
                battery.typ = typ
                battery.warranty = warranty
                battery.capacity = capacity
                battery.voltage = voltage
                battery.quantity = quantity
                battery.purchase_price = purchase_price
                battery.sell_price = sell_price

                self.db.commit()

        elif current_index == 7:
            accessory = self.db.query(Accessories).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if accessory:
                product_code = table_widget.item(selected_row, 1).text()
                product_name = table_widget.item(selected_row, 2).text()
                brand = table_widget.item(selected_row, 3).text()
                typ = table_widget.item(selected_row, 4).text()
                quantity = table_widget.item(selected_row, 5).text()
                purchase_price = table_widget.item(selected_row, 6).text()
                sell_price = table_widget.item(selected_row, 7).text()

                accessory.product_code = product_code
                accessory.product_name = product_name
                accessory.brand = brand
                accessory.typ = typ
                accessory.quantity = quantity
                accessory.purchase_price = purchase_price
                accessory.sell_price = sell_price

                self.db.commit()

        elif current_index == 8:
            labor = self.db.query(Labor).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if labor:
                labor_name = table_widget.item(selected_row, 1).text()
                start_date = table_widget.item(selected_row, 2).text()
                phon_number = table_widget.item(selected_row, 3).text()
                labor_cnic = table_widget.item(selected_row, 4).text()
                labor_address = table_widget.item(selected_row, 5).text()
                labor_pay = table_widget.item(selected_row, 6).text()

                labor.labor_name = labor_name
                labor.start_date = start_date
                labor.phon_number = phon_number
                labor.labor_cnic = labor_cnic
                labor.labor_address = labor_address
                labor.labor_pay = labor_pay

                self.db.commit()

        elif current_index == 9:
            labor = self.db.query(LaborPaid).get(int(item_id))
            QMessageBox.warning(self, "Warning", "update successfully.")
            if labor:
                labor_name = table_widget.item(selected_row, 1).text()
                labor_cnic = table_widget.item(selected_row, 2).text()
                absent_days = table_widget.item(selected_row, 3).text()
                present_days = table_widget.item(selected_row, 4).text()
                remaining_pay = table_widget.item(selected_row, 5).text()
                last_paid = table_widget.item(selected_row, 6).text()

                labor.labor_name = labor_name
                labor.labor_cnic = labor_cnic
                labor.absent_days = absent_days
                labor.present_days = present_days
                labor.remaining_pay = remaining_pay
                labor.last_paid = last_paid

                self.db.commit()
