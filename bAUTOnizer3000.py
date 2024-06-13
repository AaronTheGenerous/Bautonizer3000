# main.py

import sys
import os
import json
from datetime import datetime
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
    QDateTimeEdit,
    QTabWidget,
    QDesktopWidget,
    QDialog,
    QTimeEdit,
)
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QIcon


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
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_time(self):
        return self.time_edit.time()


class App(QWidget):
    tasks_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")

    def __init__(self):
        super().__init__()
        self.title = "Buttonizer3000"
        self.left = 100
        self.top = 100
        self.width = 230
        self.height = 550

        self.selected_time = QtCore.QTime.currentTime()

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
        tab_widget.addTab(self.init_hinzufugen_tab(), "Hinzufügen")
        tab_widget.addTab(self.init_entfernen_tab(), "Entfernen")
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        self.center_on_screen()
        self.show()

    def create_label_and_combobox(self, label_text, items):
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def init_hinzufugen_tab(self):
        hinzufugen_tab = QWidget()
        main_layout = QVBoxLayout()
        layout = QVBoxLayout()
        layout.addStretch()

        self.marken_label_hinzufugen, self.marken_hinzufugen = (
            self.create_label_and_combobox(
                "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
            )
        )
        layout.addWidget(self.marken_label_hinzufugen)
        layout.addWidget(self.marken_hinzufugen)

        self.categories_label_hinzufugen = QLabel("Kategorie", self)
        layout.addWidget(self.categories_label_hinzufugen)
        self.categories_hinzufugen = QComboBox(self)
        layout.addWidget(self.categories_hinzufugen)

        layout.addStretch()
        self.articles_label1 = QLabel("Artikelnummern (getrennt mit kommas)", self)
        layout.addWidget(self.articles_label1)
        self.articles1 = QLineEdit(self)
        layout.addWidget(self.articles1)

        self.img1_label = QLabel("Bild 1 URL (Deutsch)", self)
        layout.addWidget(self.img1_label)
        self.img1 = QLineEdit(self)
        layout.addWidget(self.img1)

        self.img2_label = QLabel("Bild 2 URL (Französisch)", self)
        layout.addWidget(self.img2_label)
        self.img2 = QLineEdit(self)
        layout.addWidget(self.img2)

        self.height_label = QLabel("Bild Höhe", self)
        layout.addWidget(self.height_label)
        self.height_box = QLineEdit(self)
        layout.addWidget(self.height_box)

        self.width_label = QLabel("Bildbreite", self)
        layout.addWidget(self.width_label)
        self.width_box = QLineEdit(self)
        layout.addWidget(self.width_box)

        self.link_checkbox = QCheckBox("Link hinzufügen?", self)
        layout.addWidget(self.link_checkbox)

        self.link_label_de = QLabel("Link (Deutsch)", self)
        layout.addWidget(self.link_label_de)
        self.link_input_de = QLineEdit(self)
        self.link_input_de.setDisabled(True)
        layout.addWidget(self.link_input_de)

        self.link_label_fr = QLabel("Link (Französisch)", self)
        layout.addWidget(self.link_label_fr)
        self.link_input_fr = QLineEdit(self)
        self.link_input_fr.setDisabled(True)
        layout.addWidget(self.link_input_fr)

        self.link_checkbox.stateChanged.connect(self.toggle_link_input)

        layout.addStretch()

        self.datetime_label = QLabel("Schedule Date", self)
        layout.addWidget(self.datetime_label)
        self.datetime_picker = QDateTimeEdit(self)
        self.datetime_picker.setCalendarPopup(True)
        self.datetime_picker.setDateTime(QDateTime.currentDateTime())
        self.datetime_picker.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(self.datetime_picker)

        self.time_button = QPushButton("Select Time", self)
        self.time_button.clicked.connect(self.open_time_picker)
        layout.addWidget(self.time_button)

        self.submit_button = QPushButton("Submit", self)
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.schedule_task)

        layout.addStretch()
        main_layout.addStretch()
        main_layout.addLayout(layout)
        main_layout.addStretch()
        hinzufugen_tab.setLayout(main_layout)

        self.update_subcategories(self.marken_hinzufugen, self.categories_hinzufugen)
        self.marken_hinzufugen.currentTextChanged.connect(
            lambda: self.update_subcategories(
                self.marken_hinzufugen, self.categories_hinzufugen
            )
        )

        return hinzufugen_tab

    def init_entfernen_tab(self):
        entfernen_tab = QWidget()
        main_layout = QVBoxLayout()
        layout = QVBoxLayout()

        self.marken_label_entfernen, self.marken_entfernen = (
            self.create_label_and_combobox(
                "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
            )
        )
        layout.addWidget(self.marken_label_entfernen)
        layout.addWidget(self.marken_entfernen)

        self.categories_label_entfernen = QLabel("Kategorie", self)
        layout.addWidget(self.categories_label_entfernen)
        self.categories_entfernen = QComboBox(self)
        layout.addWidget(self.categories_entfernen)

        self.articles_label2 = QLabel("Artikelnummern (getrennt mit kommas)", self)
        layout.addWidget(self.articles_label2)
        self.articles2 = QLineEdit(self)
        layout.addWidget(self.articles2)

        layout.addStretch()
        self.datetime_label = QLabel("Schedule Date", self)
        layout.addWidget(self.datetime_label)
        self.datetime_picker = QDateTimeEdit(self)
        self.datetime_picker.setCalendarPopup(True)
        self.datetime_picker.setDateTime(QDateTime.currentDateTime())
        self.datetime_picker.setDisplayFormat("dd.MM.yyyy HH:mm:ss")
        layout.addWidget(self.datetime_picker)

        self.time_button = QPushButton("Select Time", self)
        self.time_button.clicked.connect(self.open_time_picker)
        layout.addWidget(self.time_button)

        self.submit_button2 = QPushButton("Submit", self)
        self.submit_button2.clicked.connect(self.schedule_task)
        layout.addWidget(self.submit_button2)

        main_layout.addStretch()
        main_layout.addLayout(layout)
        main_layout.addStretch()
        entfernen_tab.setLayout(main_layout)

        self.update_subcategories(self.marken_entfernen, self.categories_entfernen)
        self.marken_entfernen.currentTextChanged.connect(
            lambda: self.update_subcategories(
                self.marken_entfernen, self.categories_entfernen
            )
        )

        return entfernen_tab

    def show_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Task scheduled successfully!")
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

    def open_time_picker(self):
        dialog = TimePickerDialog(self)
        if dialog.exec_():
            self.selected_time = dialog.get_time()

    def schedule_task(self):
        current_tab = self.tab_widget.currentIndex()
        task_type_map = {
            0: (
                "process_articles",
                self.marken_hinzufugen,
                self.categories_hinzufugen,
                self.articles1,
            ),
            1: (
                "remove_articles_images",
                self.marken_entfernen,
                self.categories_entfernen,
                self.articles2,
            ),
        }

        if current_tab not in task_type_map:
            raise ValueError(f"Invalid tab index: {current_tab}")

        task_type, marken_box, categories_box, articles_box = task_type_map[current_tab]

        schedule_date = self.datetime_picker.date().toPyDate()
        schedule_time = self.selected_time

        schedule_datetime = datetime.combine(schedule_date, schedule_time.toPyTime())

        # Print the selected date and time
        print(f"Selected date and time: {schedule_datetime}")

        task = {
            "task_type": task_type,
            "schedule_datetime": schedule_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "data": {
                "marke": marken_box.currentText(),
                "kategorie": categories_box.currentText(),
                "article_numbers": articles_box.text(),
                "img1_url": self.img1.text(),
                "img2_url": self.img2.text(),
                "width": self.width_box.text(),
                "height": self.height_box.text(),
                "link_checkbox": self.link_checkbox.isChecked(),
                "link_input_de": self.link_input_de.text(),
                "link_input_fr": self.link_input_fr.text(),
            },
        }

        task_filename = os.path.join(
            self.tasks_directory, f'task_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
        )

        os.makedirs(self.tasks_directory, exist_ok=True)

        try:
            with open(task_filename, "w") as file:
                json.dump(task, file)
            print(f"Task written to file successfully: {task_filename}")
            self.schedule_in_task_scheduler(task_filename, schedule_datetime)
        except Exception as e:
            print(f"Failed to write task to file: {e}")

        QMessageBox.information(self, "Success", "Task scheduled successfully!")

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

    def toggle_link_input(self, state):
        is_enabled = state == Qt.Checked
        self.link_input_de.setDisabled(not is_enabled)
        self.link_input_fr.setDisabled(not is_enabled)

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
