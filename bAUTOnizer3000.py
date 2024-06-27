# bAUTOnizer3000.py

import sys
import os
import json
import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QCheckBox,
    QTabWidget,
    QDesktopWidget,
    QDialog,
    QTimeEdit,
    QCalendarWidget,
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon, QFont


class TimePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Time")
        self.layout = QVBoxLayout()
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QtCore.QTime.currentTime())
        self.layout.addWidget(self.time_edit)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.confirm_time)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def confirm_time(self):
        self.selected_time = self.time_edit.time()
        self.accept()

    def get_time(self):
        return self.selected_time


class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.layout = QVBoxLayout()

        self.calendar_widget = QCalendarWidget()
        self.layout.addWidget(self.calendar_widget)

        confirm_button = QPushButton("OK")
        confirm_button.clicked.connect(self.confirm_date)
        self.layout.addWidget(confirm_button)

        self.selected_date = QDate.currentDate()

        self.setLayout(self.layout)

    def confirm_date(self):
        self.selected_date = self.calendar_widget.selectedDate()
        self.accept()

    def get_date(self):
        return self.selected_date


class App(QWidget):
    tasks_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")
    last_task_end_time_file = os.path.join(tasks_directory, "last_task_end_time.json")

    def __init__(self):
        super().__init__()
        self.title = "Buttonizer3000"
        self.left = 100
        self.top = 100
        self.width = 230
        self.height = 550

        self.selected_date = QDate.currentDate()
        self.selected_time = QTime.currentTime()

        self.category_data = {
            "Kamerasysteme + Objektive": {
                "Nikon": {
                    "Nikon Z": {},
                    "Nikkor Z-Mount Objektive": {},
                    "Nikon DSLR": {},
                    "Nikkor F-Mount Objektive": {},
                    "Nikon Blitzgeräte": {},
                    "Nikon Coolpix": {},
                    "Nikon DSLR Zubehör": {},
                    "Nikon Objektivzubehör": {},
                },
                "Sony": {
                    "Sony E-Mount Kameras": {},
                    "Sony E-Mount Objektive": {},
                    "Sony E-Mount APS-C Kameras": {},
                    "Sony E-Mount APS-C Objektive": {},
                    "Sony E-Mount Zubehör": {},
                    "Sony Blitzgeräte": {},
                    "Sony Kompaktkameras": {},
                    "Sony XPERIA Smartphones": {},
                    "Sony A-Mount Kameras": {},
                    "Sony A-Mount Objektive": {},
                    "Sony A-Mount Zubehör": {},
                },
                "Phase One": {
                    "Phase One IQ Backs": {},
                    "Phase One XF Camera System": {},
                    "Phase One XT Camera System": {},
                    "CPO Phase One IQ Backs für Phase One XF": {},
                    "CPO Phase One XF Kamerasysteme": {},
                    "CPO Phase One IQ Backs für Hasselblad": {},
                    "Phase One XF Kamerasysteme": {},
                    "Phase One XT Kamera und Objektive": {},
                    "Schneider Kreuznach Objektive (Blue Ring)": {},
                    "CPO Schneider Kreuznach Objektive": {},
                    "Capture One": {},
                },
                "Cambo": {
                    "Cambo Wide RS": {},
                    "Cambo ACTUS": {},
                    "Cambo Zubehör zu Phase One XT": {},
                    "Cambo Adapter": {},
                    "Cambo ACTUS DB": {},
                    "Cambo ACTUS-XL": {},
                },
                "Leica": {
                    "Leica M & Objektive": {},
                    "Leica Q": {},
                    "Leica SL & Objektive": {},
                    "Leica S & Objektive": {},
                    "Leica TL / CL & Objektive": {},
                    "Leica V": {},
                    "Leica X": {},
                    "Leica SOFORT": {},
                },
            }
        }

        self.display_label_title = QLabel("Geplantes Datum und Uhrzeit")
        font2 = QFont()
        font2.setPointSize(10)
        self.display_label_title.setFont(font2)
        self.display_label_title.setStyleSheet(
            """
            QLabel {
                background-color: #f9f9f9;
                font-weight: bold;
                border: 2px solid #ffdd00;
                padding: 5px;
            }
        """
        )
        self.display_label_title.setAlignment(Qt.AlignCenter)

        self.datetime_label = QLabel(self)
        font = QFont()
        font.setPointSize(15)
        self.datetime_label.setFont(font)
        self.datetime_label.setStyleSheet(
            """
            QLabel {
                background-color: #f9f9f9;
                border: 2px solid #ffdd00;
                padding: 5px;
            }
        """
        )
        self.datetime_label.setAlignment(Qt.AlignCenter)
        self.update_datetime_label()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(
            QIcon(
                r"C:\Users\Hafner\Desktop\Aaron_C\Files_Software\Buttonizer3000\Bautonizer\NIK Buttons 10 CH.ico"
            )
        )

        layout = QVBoxLayout()
        tab_widget = QTabWidget()
        self.tab_widget = tab_widget
        tab_widget.addTab(
            self.create_tab("Hinzufügen", self.schedule_task), "Hinzufügen"
        )
        tab_widget.addTab(self.create_tab("Entfernen", self.schedule_task), "Entfernen")
        layout.addWidget(tab_widget)

        layout.addWidget(self.display_label_title)
        layout.addWidget(self.datetime_label)

        self.setLayout(layout)
        self.center_on_screen()
        self.show()

    def create_label_and_combobox(self, label_text, items):
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def open_date_picker(self):
        dialog = DatePickerDialog(self)
        if dialog.exec_():
            self.selected_date = dialog.get_date()
            print(f"Selected Date: {self.selected_date.toString('dd/MM/yyyy')}")
            self.update_datetime_label()

    def open_time_picker(self):
        dialog = TimePickerDialog(self)
        if dialog.exec_():
            self.selected_time = dialog.get_time()
            print(f"Selected Time: {self.selected_time.toString('HH:mm:ss')}")
            self.update_datetime_label()

    def update_datetime_label(self):
        selected_date = self.selected_date.toString("dd/MM/yyyy")
        selected_time = self.selected_time.toString("HH:mm:ss")
        print(f"Updating Label with: {selected_date} {selected_time}")
        self.datetime_label.setText(f"{selected_date} \n{selected_time}")

    def create_tab(self, tab_name, submit_action):
        tab = QWidget()
        main_layout = QVBoxLayout()
        layout = QVBoxLayout()
        layout.addStretch()

        marken_label, marken_combobox = self.create_label_and_combobox(
            "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
        )
        layout.addWidget(marken_label)
        layout.addWidget(marken_combobox)

        categories_label, categories_combobox = self.create_label_and_combobox(
            "Kategorie", []
        )
        layout.addWidget(categories_label)
        layout.addWidget(categories_combobox)

        layout.addStretch()
        articles_input = self.create_line_edit_with_label(
            "Artikelnummern (getrennt mit Kommas)", layout
        )
        layout.addWidget(articles_input)

        if tab_name == "Hinzufügen":
            self.add_image_and_link_fields(layout)

        self.add_datetime_fields(layout)

        self.run_after_previous_checkbox = QCheckBox("Run after previous task", self)
        layout.addWidget(self.run_after_previous_checkbox)

        submit_button = QPushButton("Bestätigen", self)
        submit_button.clicked.connect(
            lambda: submit_action(
                marken_combobox, categories_combobox, articles_input, tab_name
            )
        )
        layout.addWidget(submit_button)

        layout.addStretch()
        main_layout.addStretch()
        main_layout.addLayout(layout)
        main_layout.addStretch()
        tab.setLayout(main_layout)

        self.update_subcategories(marken_combobox, categories_combobox)
        marken_combobox.currentTextChanged.connect(
            lambda: self.update_subcategories(marken_combobox, categories_combobox)
        )

        return tab

    def add_image_and_link_fields(self, layout):
        fields = [
            ("Bild 1 URL (Deutsch)", "img1_input"),
            ("Bild 2 URL (Französisch)", "img2_input"),
            ("Bild Höhe", "height_input"),
            ("Bildbreite", "width_input"),
        ]
        for label_text, attr_name in fields:
            setattr(
                self, attr_name, self.create_line_edit_with_label(label_text, layout)
            )
            layout.addWidget(getattr(self, attr_name))

        self.link_checkbox = QCheckBox("Link hinzufügen?", self)
        layout.addWidget(self.link_checkbox)

        self.link_input_de = self.create_line_edit_with_label("Link (Deutsch)", layout)
        self.link_input_de.setDisabled(True)
        layout.addWidget(self.link_input_de)

        self.link_input_fr = self.create_line_edit_with_label(
            "Link (Französisch)", layout
        )
        self.link_input_fr.setDisabled(True)
        layout.addWidget(self.link_input_fr)

        self.link_checkbox.stateChanged.connect(
            lambda state: self.toggle_link_input(
                state, self.link_input_de, self.link_input_fr
            )
        )

    def create_line_edit_with_label(self, label_text, layout):
        label = QLabel(label_text, self)
        layout.addWidget(label)
        return QLineEdit(self)

    def add_datetime_fields(self, layout):
        dateTime_title_label = QLabel("Datum & Uhrzeit planen", self)
        dateTime_title_label.setAlignment(Qt.AlignCenter)
        dateTime_title_label.setStyleSheet(
            """
            QLabel{
                font-weight: bold;
            }
        """
        )
        layout.addWidget(dateTime_title_label)

        buttons = [
            ("Datum wählen", self.open_date_picker),
            ("Uhrzeit wählen", self.open_time_picker),
        ]
        for text, handler in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(handler)
            layout.addWidget(button)

    def show_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Geschafft")
        msg_box.setText(
            "Task erfolgreich geplant. \nDu siehst heute übrigens mal wieder super aus <3"
        )
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() in [
            Qt.Key_Enter,
            Qt.Key_Return,
        ]:
            current_tab_index = self.tab_widget.currentIndex()
            if current_tab_index == 0:
                self.submit_button.click()
            elif current_tab_index == 1:
                self.submit_button2.click()
            return True
        return super().eventFilter(obj, event)

    def schedule_task(self, marken_box, categories_box, articles_input, tab_name):
        task_type = (
            "process_articles" if tab_name == "Hinzufügen" else "remove_articles_images"
        )

        task = {
            "task_type": task_type,
            "data": {
                "marke": marken_box.currentText(),
                "kategorie": categories_box.currentText(),
                "article_numbers": articles_input.text(),
                "img1_url": (
                    self.img1_input.text() if tab_name == "Hinzufügen" else None
                ),
                "img2_url": (
                    self.img2_input.text() if tab_name == "Hinzufügen" else None
                ),
                "width": self.width_input.text() if tab_name == "Hinzufügen" else None,
                "height": (
                    self.height_input.text() if tab_name == "Hinzufügen" else None
                ),
                "link_checkbox": (
                    self.link_checkbox.isChecked() if tab_name == "Hinzufügen" else None
                ),
                "link_input_de": (
                    self.link_input_de.text() if tab_name == "Hinzufügen" else None
                ),
                "link_input_fr": (
                    self.link_input_fr.text() if tab_name == "Hinzufügen" else None
                ),
            },
        }

        task_filename = os.path.join(
            self.tasks_directory,
            f'task_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json',
        )

        os.makedirs(self.tasks_directory, exist_ok=True)

        try:
            with open(task_filename, "w") as file:
                json.dump(task, file)
            print(f"Task written to file successfully: {task_filename}")

            if self.run_after_previous_checkbox.isChecked():
                start_time = self.get_last_task_end_time() + datetime.timedelta(
                    seconds=1
                )
            else:
                start_time = datetime.datetime(
                    self.selected_date.year(),
                    self.selected_date.month(),
                    self.selected_date.day(),
                    self.selected_time.hour(),
                    self.selected_time.minute(),
                    self.selected_time.second(),
                )

            task_duration = datetime.timedelta(
                minutes=5
            )  # Assuming each task takes 5 minutes
            self.set_last_task_end_time(start_time + task_duration)

            self.schedule_in_task_scheduler(task_filename, start_time)
        except Exception as e:
            print(f"Failed to write task to file: {e}")

        QMessageBox.information(self, "Success", "Task scheduled successfully!")

    def get_last_task_end_time(self):
        if os.path.exists(self.last_task_end_time_file):
            with open(self.last_task_end_time_file, "r") as file:
                last_task_end_time = datetime.datetime.fromisoformat(file.read())
        else:
            last_task_end_time = datetime.datetime.now()

        return last_task_end_time

    def set_last_task_end_time(self, end_time):
        with open(self.last_task_end_time_file, "w") as file:
            file.write(end_time.isoformat())

    def schedule_in_task_scheduler(self, task_filename, schedule_datetime):
        import subprocess

        date_str = schedule_datetime.strftime("%d/%m/%Y")
        time_str = schedule_datetime.strftime("%H:%M")

        command = f'SchTasks /Create /SC ONCE /TN "ButtonizerTask_{os.path.basename(task_filename)}" /TR "python {os.path.abspath(__file__).replace("main.py", "execute_task.py")} {task_filename}" /ST {time_str} /SD {date_str} /F'

        print(f"Scheduling command: {command}")

        try:
            subprocess.run(command, check=True, shell=True)
            print("Scheduled task successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to schedule task: {e}")

    def toggle_link_input(self, state, link_input_de, link_input_fr):
        is_enabled = state == Qt.Checked
        link_input_de.setDisabled(not is_enabled)
        link_input_fr.setDisabled(not is_enabled)

    def center_on_screen(self):
        qr = self.frameGeometry()
        screen_geometry = QDesktopWidget().availableGeometry()
        cp = screen_geometry.center()
        cp.setX(int(screen_geometry.width() * 3 / 4 - qr.width() / 4))
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_subcategories(self, marken_box, categories_box):
        current_brand = marken_box.currentText()
        categories_box.clear()
        if current_brand in self.category_data["Kamerasysteme + Objektive"]:
            categories_box.addItems(
                self.category_data["Kamerasysteme + Objektive"][current_brand].keys()
            )
            categories_box.setCurrentIndex(0)
            categories_box.setDisabled(False)
        else:
            categories_box.addItem("Keine Kategorien verfügbar")
            categories_box.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
