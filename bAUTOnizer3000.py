import sys
import os
import json
import datetime
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QTabWidget,
    QDialog,
    QTimeEdit,
    QCalendarWidget,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QIcon, QFont


class App(QWidget):
    tasks_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")
    last_task_end_time_file = os.path.join(tasks_directory, "last_task_end_time.json")
    multi_mode = False  # Track if multi-mode is enabled

    def __init__(self):
        super().__init__()
        self.title = "Buttonizer3000"
        self.left = 100
        self.top = 100
        self.width = 230
        self.height = 600  # Increased height to accommodate the switch and banner

        self.selected_date = QDate.currentDate()
        self.selected_time = QTime.currentTime()

        self.temp_tasks = []  # Temporary storage for tasks in multi-task mode

        self.button_layouts = {}  # Temporary storage for each button layout

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
        self.setWindowIcon(QIcon(r"C:\path\to\icon.ico"))

        self.main_layout = QVBoxLayout()

        # Create the switch for Single-Task Mode and Multi-Task Mode
        self.create_mode_switch(self.main_layout)

        # New banner label at the very top
        self.top_banner_label = self.create_label("", 10, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.top_banner_label)

        self.banner_label = self.create_label("", 10, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.banner_label)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: 2px solid #ffffff; }")
        self.tab_widget.addTab(
            self.create_tab("Hinzufügen", self.schedule_task), "Hinzufügen"
        )
        self.tab_widget.addTab(
            self.create_tab("Entfernen", self.schedule_task), "Entfernen"
        )
        self.main_layout.addWidget(self.tab_widget)

        self.display_label_title = self.create_label(
            "<b>Geplantes Datum und Uhrzeit</b>", 10, Qt.AlignmentFlag.AlignCenter, True
        )
        self.main_layout.addWidget(self.display_label_title)

        self.datetime_label = self.create_label(
            "", 15, Qt.AlignmentFlag.AlignCenter, True
        )
        self.update_datetime_label()
        self.main_layout.addWidget(self.datetime_label)

        self.setLayout(self.main_layout)
        self.center_on_screen()
        self.show()

    def create_mode_switch(self, layout):
        self.single_task_radio = QRadioButton("Single-Task Mode")
        self.multi_task_radio = QRadioButton("Multi-Task Mode")

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.single_task_radio)
        self.button_group.addButton(self.multi_task_radio)
        self.single_task_radio.setChecked(True)  # Default to Single-Task Mode

        self.single_task_radio.toggled.connect(self.toggle_multi_mode)
        self.multi_task_radio.toggled.connect(self.toggle_multi_mode)

        switch_layout = QHBoxLayout()
        switch_layout.addWidget(self.single_task_radio)
        switch_layout.addWidget(self.multi_task_radio)
        layout.addLayout(switch_layout)

    def toggle_multi_mode(self):
        self.multi_mode = self.multi_task_radio.isChecked()
        self.tab_widget.setStyleSheet(
            "QTabWidget::pane { border: 2px solid #ffdd00; }"
            if self.multi_mode
            else "QTabWidget::pane { border: 2px solid #ffffff; }"
        )
        self.banner_label.setText(
            "<b>Multi-Task Mode</b>" + "<br>" + "Startzeit und Datum Wählen"
            if self.multi_mode
            else ""
        )
        self.top_banner_label.hide()  # Hide the new top banner when switching modes

        for tab_name in self.button_layouts:
            self.update_buttons(tab_name)
        self.update_ui_elements()

    def update_buttons(self, tab_name):
        button_layout = self.button_layouts[tab_name]
        self.clear_layout(button_layout)
        if self.multi_mode:
            next_task_button = self.create_button(
                "Next Task", self.save_task_temporarily
            )
            plan_tasks_button = self.create_button("Tasks Planen", self.save_all_tasks)
            button_layout.addWidget(next_task_button)
            button_layout.addWidget(plan_tasks_button)
        else:
            submit_button = self.create_button(
                "Bestätigen",
                lambda: self.schedule_task(
                    self.marken_combobox,
                    self.categories_combobox,
                    self.articles_input,
                    tab_name,
                ),
            )
            button_layout.addWidget(submit_button)

    def update_ui_elements(self):
        if self.multi_mode and len(self.temp_tasks) == 0:
            self.show_datetime_fields()
        elif self.multi_mode and len(self.temp_tasks) > 0:
            self.hide_datetime_fields()
        else:
            self.show_datetime_fields()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_tab(self, tab_name, submit_action):
        tab = QWidget()
        layout = QVBoxLayout()

        self.current_tab_name = tab_name
        marken_label, marken_combobox = self.create_label_and_combobox(
            "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
        )
        layout.addWidget(marken_label)
        layout.addWidget(marken_combobox)
        self.marken_combobox = marken_combobox

        categories_label, categories_combobox = self.create_label_and_combobox(
            "Kategorie", []
        )
        layout.addWidget(categories_label)
        layout.addWidget(categories_combobox)
        self.categories_combobox = categories_combobox

        layout.addStretch()
        articles_input = self.create_line_edit_with_label(
            "Artikelnummern (getrennt mit Kommas)", layout
        )
        layout.addWidget(articles_input)
        self.articles_input = articles_input

        if tab_name == "Hinzufügen":
            self.add_image_and_link_fields(layout)

        self.add_datetime_fields(layout)

        button_layout = QVBoxLayout()
        self.button_layouts[tab_name] = button_layout  # Store the button layout
        self.update_buttons(tab_name)
        layout.addLayout(button_layout)

        self.update_subcategories(marken_combobox, categories_combobox)
        marken_combobox.currentTextChanged.connect(
            lambda: self.update_subcategories(marken_combobox, categories_combobox)
        )

        tab.setLayout(layout)

        return tab

    def create_label_and_combobox(self, label_text, items):
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def create_line_edit_with_label(self, label_text, layout):
        label = QLabel(label_text, self)
        layout.addWidget(label)
        return QLineEdit(self)

    def create_label(self, text, font_size, alignment, with_border=False):
        label = QLabel(text, self)
        font = QFont()
        font.setPointSize(font_size)
        label.setFont(font)
        label.setAlignment(alignment)
        if with_border:
            label.setStyleSheet("border: 2px solid #ffdd00;")
        return label

    def create_button(self, text, click_handler):
        button = QPushButton(text, self)
        button.clicked.connect(click_handler)
        return button

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

    def add_datetime_fields(self, layout):
        self.dateTime_title_label = QLabel("<b>Datum & Uhrzeit planen</b>", self)
        self.dateTime_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dateTime_title_label.setStyleSheet(
            """
            QLabel{
                font-weight: bold;
            }
        """
        )
        layout.addWidget(self.dateTime_title_label)

        buttons = [
            ("Datum wählen", self.open_date_picker),
            ("Uhrzeit wählen", self.open_time_picker),
        ]
        self.datetime_buttons = []
        for text, handler in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(handler)
            layout.addWidget(button)
            self.datetime_buttons.append(button)

    def open_date_picker(self):
        dialog = DatePickerDialog(self)
        if dialog.exec():
            self.selected_date = dialog.get_date()
            self.update_datetime_label()

    def open_time_picker(self):
        dialog = TimePickerDialog(self)
        if dialog.exec():
            self.selected_time = dialog.get_time()
            self.update_datetime_label()

    def update_datetime_label(self):
        selected_date = self.selected_date.toString("dd/MM/yyyy")
        selected_time = self.selected_time.toString("HH:mm:ss")
        self.datetime_label.setText(f"{selected_date} \n{selected_time}")

    def show_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Geschafft")
        msg_box.setText(
            "Task erfolgreich geplant. \nDu siehst heute übrigens mal wieder super aus <3"
        )
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() in [
            Qt.Key.Key_Enter,
            Qt.Key.Key_Return,
        ]:
            current_tab_index = self.tab_widget.currentIndex()
            if current_tab_index == 0:
                self.submit_button.click()
            elif current_tab_index == 1:
                self.submit_button2.click()
            return True
        return super().eventFilter(obj, event)

    def save_task_temporarily(self):
        task = self.create_task()
        self.temp_tasks.append(task)
        self.clear_input_fields()
        if len(self.temp_tasks) == 1:
            self.banner_label.setText(
                "<b>Multi-Task Mode</b>" + "<br>" + "Nach dem ersten Task ausführen"
            )
            self.hide_datetime_fields()
        # Show the new top banner
        self.top_banner_label.setText("Task saved! Click 'Next Task' to add another.")
        self.top_banner_label.show()

    def save_all_tasks(self):
        task_directory = self.tasks_directory
        os.makedirs(task_directory, exist_ok=True)

        initial_task = self.temp_tasks[0]
        initial_task["subsequent_tasks"] = []

        for idx, task in enumerate(self.temp_tasks):
            task_filename = os.path.join(
                task_directory,
                f'task_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{idx}.json',
            )
            with open(task_filename, "w") as file:
                json.dump(task, file)
            if idx > 0:
                initial_task["subsequent_tasks"].append(task_filename)

        initial_task_filename = os.path.join(
            task_directory,
            f'task_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_initial.json',
        )
        with open(initial_task_filename, "w") as file:
            json.dump(initial_task, file)

        # Schedule the initial task
        schedule_datetime = datetime.datetime.fromisoformat(
            initial_task["schedule_datetime"]
        )
        self.schedule_in_task_scheduler(initial_task_filename, schedule_datetime)

        self.temp_tasks = []  # Clear the temporary tasks
        self.show_message()

    def schedule_task(self, marken_box, categories_box, articles_input, tab_name):
        task = self.create_task()

        task_filename = os.path.join(
            self.tasks_directory,
            f'task_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json',
        )

        os.makedirs(self.tasks_directory, exist_ok=True)

        with open(task_filename, "w") as file:
            json.dump(task, file)

        if not self.multi_mode:
            # Convert schedule_datetime from string to datetime object
            schedule_datetime = datetime.datetime.fromisoformat(
                task["schedule_datetime"]
            )
            self.schedule_in_task_scheduler(task_filename, schedule_datetime)

        # Show the confirmation banner
        self.show_confirmation_banner("Task created")

        QMessageBox.information(self, "Success", "Task scheduled successfully!")

    def create_task(self):
        task = {
            "marken": self.marken_combobox.currentText(),
            "categories": self.categories_combobox.currentText(),
            "articles": self.articles_input.text(),
            "schedule_datetime": f"{self.selected_date.toString('yyyy-MM-dd')}T{self.selected_time.toString('HH:mm:ss')}",
        }
        return task

    def show_confirmation_banner(self, message):
        self.banner_label.setText(message)
        self.banner_label.show()

        # Create the animation
        self.animation = QPropertyAnimation(self.banner_label, b"geometry")
        self.animation.setDuration(1000)  # Duration of the animation in milliseconds
        self.animation.setStartValue(
            QRect(-self.width(), 0, self.width(), 30)
        )  # Start off-screen
        self.animation.setEndValue(
            QRect(0, 0, self.width(), 30)
        )  # End at the top of the window
        self.animation.start()

        # Hide the banner after a delay
        QtCore.QTimer.singleShot(3000, self.banner_label.hide)  # Hide after 3 seconds

    def schedule_in_task_scheduler(self, task_filename, schedule_datetime):
        import subprocess

        date_str = schedule_datetime.strftime("%d/%m/%Y")
        time_str = schedule_datetime.strftime("%H:%M")
        command = f'SchTasks /Create /SC ONCE /TN "ButtonizerTask_{os.path.basename(task_filename)}" /TR "python {os.path.abspath(__file__).replace("bAUTOnizer3000.py", "exe_tasks.py")} {task_filename}" /ST {time_str} /SD {date_str} /F'
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to schedule task: {e}")

    def clear_input_fields(self):
        self.marken_combobox.setCurrentIndex(0)
        self.categories_combobox.setCurrentIndex(0)
        self.articles_input.clear()

    def hide_datetime_fields(self):
        self.dateTime_title_label.hide()
        for button in self.datetime_buttons:
            button.hide()

    def update_subcategories(self, marken_combobox, categories_combobox):
        selected_marke = marken_combobox.currentText()
        categories_combobox.clear()
        if selected_marke in self.category_data["Kamerasysteme + Objektive"]:
            categories_combobox.addItems(
                self.category_data["Kamerasysteme + Objektive"][selected_marke].keys()
            )

    def toggle_link_input(self, state, link_input_de, link_input_fr):
        if state == Qt.CheckState.Checked:
            link_input_de.setDisabled(False)
            link_input_fr.setDisabled(False)
        else:
            link_input_de.setDisabled(True)
            link_input_fr.setDisabled(True)

    def center_on_screen(self):
        resolution = QApplication.primaryScreen().geometry()
        x = (resolution.width() - self.width) // 2
        y = (resolution.height() - self.height) // 2
        self.move(x, y)

    def hide_datetime_fields(self):
        self.dateTime_title_label.hide()
        for button in self.datetime_buttons:
            button.hide()
        self.display_label_title.hide()
        self.datetime_label.hide()

    def show_datetime_fields(self):
        self.dateTime_title_label.show()
        for button in self.datetime_buttons:
            button.show()
        self.display_label_title.show()
        self.datetime_label.show()


class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Datum wählen")
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def get_date(self):
        return self.calendar.selectedDate()


class TimePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Uhrzeit wählen")
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        layout = QVBoxLayout(self)
        layout.addWidget(self.time_edit)
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def get_time(self):
        return self.time_edit.time()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
