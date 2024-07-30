import datetime
import json
import os
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QDate, QTime, QEasingCurve, QPropertyAnimation
from PyQt6.QtGui import QIcon, QFont, QColor, QPainter, QPen
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


class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = None
        self.calendar = None
        self.setWindowTitle("Datum wählen")
        self.create_calendar_widget()
        self.create_buttons()

    def create_calendar_widget(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.calendar)

    def create_buttons(self):
        buttons = QHBoxLayout()
        ok_button = self.create_button("OK", self.accept)
        cancel_button = self.create_button("Abbrechen", self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        self.layout.addLayout(buttons)

    def create_button(self, text, handler):
        button = QPushButton(text, self)
        button.clicked.connect(handler)
        return button

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


class App(QWidget):
    tasks_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")
    last_task_end_time_file = os.path.join(tasks_directory, "last_task_end_time.json")
    multi_mode = False  # Track if multi-mode is enabled

    def __init__(self):
        super().__init__()
        self.title = "Buttonizer3000"
        self.left = 100
        self.top = 100
        self.window_width = 260
        self.height = 880  # Increased height to accommodate the switch and banner
        self.borderColor = QColor(
            255, 221, 0, 0
        )  # Initial border color (transparent yellow)

        self.selected_date = QDate.currentDate()
        self.selected_time = QTime.currentTime()

        self.temp_tasks = []  # Temporary storage for tasks in multi-task mode

        self.button_layouts = {}  # Temporary storage for each button layout

        self.datetime_layout = QVBoxLayout()
        self.datetime_widgets = []
        self.datetime_fields_added = False

        # Separate instances for each tab
        self.articles_input_add = None
        self.articles_input_remove = None
        self.marken_combobox_add = None
        self.marken_combobox_remove = None
        self.categories_combobox_add = None
        self.categories_combobox_remove = None

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
        self.setGeometry(self.left, self.top, self.window_width, self.height)
        self.setFixedSize(self.window_width, self.height)
        self.setWindowIcon(QIcon(r"C:\path\to\icon.ico"))

        self.main_layout = QVBoxLayout()

        # Create the switch for Single-Task Mode and Multi-Task Mode
        self.create_mode_switch(self.main_layout)

        self.clear_checkbox = QCheckBox("Clear Input", self)
        self.clear_checkbox.setChecked(True)  # The checkbox is checked by default
        # Create a QHBoxLayout for checkbox and add spacers to both sides.
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch(1)  # Add spacer on the left
        checkbox_layout.addWidget(self.clear_checkbox)
        checkbox_layout.addStretch(1)  # Add spacer on the right

        # New banner label at the very top
        self.top_banner_label = self.create_label("", 10, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.top_banner_label)

        self.banner_label = self.create_label("", 10, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.banner_label)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget::pane { border: 2px solid #ffffff; }")
        self.tab_widget.addTab(
            self.create_tab("Hinzufügen", self.schedule_task, "add"), "Hinzufügen"
        )
        self.tab_widget.addTab(
            self.create_tab("Entfernen", self.schedule_task, "remove"), "Entfernen"
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

        self.main_layout.addLayout(self.datetime_layout)

        self.main_layout.addLayout(checkbox_layout)

        self.setLayout(self.main_layout)
        self.center_on_screen()
        self.show()

        # Debug statements
        print(
            f"Initialized UI with tab_widget: {self.tab_widget}, id: {id(self.tab_widget)}"
        )

    def add_datetime_fields(self, layout):
        if not self.datetime_fields_added:
            buttons = [
                ("Datum wählen", self.open_date_picker),
                ("Uhrzeit wählen", self.open_time_picker),
            ]
            self.datetime_buttons = []
            for text, handler in buttons:
                button = QPushButton(text, self)
                button.clicked.connect(handler)
                self.datetime_layout.addWidget(button)
                self.datetime_widgets.append(button)
            self.datetime_fields_added = True

    def add_articles_input(self, layout, tab_type):
        if tab_type == "add":
            self.articles_input_add = self.create_line_edit_with_label(
                "Artikelnummern (getrennt mit Kommas)", layout
            )
            layout.addWidget(self.articles_input_add)
            self.articles_input_add.textChanged.connect(self.on_articles_input_changed)
            print(
                f"Initialized articles_input_add: {self.articles_input_add}, id: {id(self.articles_input_add)}, text: {self.articles_input_add.text()}"
            )  # Debug line
        elif tab_type == "remove":
            self.articles_input_remove = self.create_line_edit_with_label(
                "Artikelnummern (getrennt mit Kommas)", layout
            )
            layout.addWidget(self.articles_input_remove)
            self.articles_input_remove.textChanged.connect(
                self.on_articles_input_changed
            )
            print(
                f"Initialized articles_input_remove: {self.articles_input_remove}, id: {id(self.articles_input_remove)}, text: {self.articles_input_remove.text()}"
            )  # Debug line

    def add_image_and_link_fields(self, layout):
        self.img1_input = self.create_line_edit_with_label(
            "Bild 1 URL (Deutsch)", layout
        )
        layout.addWidget(self.img1_input)
        self.img2_input = self.create_line_edit_with_label(
            "Bild 2 URL (Französisch)", layout
        )
        layout.addWidget(self.img2_input)
        self.height_input = self.create_line_edit_with_label("Bild Höhe", layout)
        layout.addWidget(self.height_input)
        self.width_input = self.create_line_edit_with_label("Bildbreite", layout)
        layout.addWidget(self.width_input)

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

    def on_articles_input_changed(self, text):
        print(f"articles_input changed: {text}")

    def add_marken_and_categories(self, layout, tab_type):
        if tab_type == "add":
            marken_label, self.marken_combobox_add = self.create_label_and_combobox(
                "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
            )
            layout.addWidget(marken_label)
            layout.addWidget(self.marken_combobox_add)

            categories_label, self.categories_combobox_add = (
                self.create_label_and_combobox("Kategorie", [])
            )
            layout.addWidget(categories_label)
            layout.addWidget(self.categories_combobox_add)

            self.update_subcategories(
                self.marken_combobox_add, self.categories_combobox_add
            )
            self.marken_combobox_add.currentTextChanged.connect(
                lambda: self.update_subcategories(
                    self.marken_combobox_add, self.categories_combobox_add
                )
            )
            self.marken_combobox_add.currentTextChanged.connect(
                self.on_marken_combobox_changed
            )
            self.categories_combobox_add.currentTextChanged.connect(
                self.on_categories_combobox_changed
            )

        elif tab_type == "remove":
            marken_label, self.marken_combobox_remove = self.create_label_and_combobox(
                "Marke", self.category_data["Kamerasysteme + Objektive"].keys()
            )
            layout.addWidget(marken_label)
            layout.addWidget(self.marken_combobox_remove)

            categories_label, self.categories_combobox_remove = (
                self.create_label_and_combobox("Kategorie", [])
            )
            layout.addWidget(categories_label)
            layout.addWidget(self.categories_combobox_remove)

            self.update_subcategories(
                self.marken_combobox_remove, self.categories_combobox_remove
            )
            self.marken_combobox_remove.currentTextChanged.connect(
                lambda: self.update_subcategories(
                    self.marken_combobox_remove, self.categories_combobox_remove
                )
            )
            self.marken_combobox_remove.currentTextChanged.connect(
                self.on_marken_combobox_changed
            )
            self.categories_combobox_remove.currentTextChanged.connect(
                self.on_categories_combobox_changed
            )

    def on_marken_combobox_changed(self, text):
        print(f"marken_combobox changed: {text}")

    def on_categories_combobox_changed(self, text):
        print(f"categories_combobox changed: {text}")

    def center_on_screen(self):
        resolution = QApplication.primaryScreen().geometry()
        x = (resolution.width() - self.window_width) // 2
        y = (resolution.height() - self.height) // 2
        self.move(x, y)

    def clear_input_fields(self):
        clear_fields = self.clear_checkbox.isChecked()
        if clear_fields:
            current_tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
            if current_tab_name == "Hinzufügen":
                self.marken_combobox_add.setCurrentIndex(0)
                self.categories_combobox_add.setCurrentIndex(0)
                print(
                    f"Before clearing (Hinzufügen): articles_input: {self.articles_input_add.text()}, id: {id(self.articles_input_add)}, img1_input: {self.img1_input.text()}, img2_input: {self.img2_input.text()}"
                )
                self.articles_input_add.clear()
                self.img1_input.clear()
                self.img2_input.clear()
                self.width_input.clear()
                self.height_input.clear()
                self.link_checkbox.setChecked(False)
                self.link_input_de.clear()
                self.link_input_fr.clear()
                print(
                    f"After clearing (Hinzufügen): articles_input: {self.articles_input_add.text()}, id: {id(self.articles_input_add)}"
                )
            elif current_tab_name == "Entfernen":
                self.marken_combobox_remove.setCurrentIndex(0)
                self.categories_combobox_remove.setCurrentIndex(0)
                print(
                    f"Before clearing (Entfernen): articles_input: {self.articles_input_remove.text()}, id: {id(self.articles_input_remove)}"
                )
                self.articles_input_remove.clear()
                print(
                    f"After clearing (Entfernen): articles_input: {self.articles_input_remove.text()}, id: {id(self.articles_input_remove)}"
                )

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_button(self, text, click_handler):
        button = QPushButton(text, self)
        button.clicked.connect(click_handler)
        return button

    def create_label(self, text, font_size, alignment, with_border=False):
        label = QLabel(text, self)
        font = QFont()
        font.setPointSize(font_size)
        label.setFont(font)
        label.setAlignment(alignment)
        if with_border:
            label.setStyleSheet("border: 2px solid #ffdd00;")
        return label

    def create_label_and_combobox(self, label_text, items):
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def create_line_edit_with_label(self, label_text, layout):
        label = QLabel(label_text, self)
        layout.addWidget(label)
        return QLineEdit(self)

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

    def create_tab(self, tab_name, submit_action, tab_type):
        tab = QWidget()
        layout = QVBoxLayout()

        self.current_tab_name = tab_name
        print(f"Creating tab: {tab_name}, id: {id(tab_name)}")

        self.add_marken_and_categories(layout, tab_type)
        self.add_articles_input(layout, tab_type)

        if tab_type == "add":
            self.add_image_and_link_fields(layout)

        self.add_datetime_fields(layout)

        button_layout = QVBoxLayout()
        self.button_layouts[tab_name] = button_layout  # Store the button layout
        self.update_buttons(tab_name)
        layout.addLayout(button_layout)

        tab.setLayout(layout)

        # Debug statements
        print(
            f"Tab {tab_name} created with marken_combobox: {self.marken_combobox_add if tab_type == 'add' else self.marken_combobox_remove}, id: {id(self.marken_combobox_add if tab_type == 'add' else self.marken_combobox_remove)}, categories_combobox: {self.categories_combobox_add if tab_type == 'add' else self.categories_combobox_remove}, id: {id(self.categories_combobox_add if tab_type == 'add' else self.categories_combobox_remove)}, articles_input: {self.articles_input_add if tab_type == 'add' else self.articles_input_remove}, id: {id(self.articles_input_add if tab_type == 'add' else self.articles_input_remove)}"
        )

        return tab

    def create_task(self):
        print("create_task called")
        current_tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        articles_input = (
            self.articles_input_add
            if current_tab_name == "Hinzufügen"
            else self.articles_input_remove
        )
        marken_combobox = (
            self.marken_combobox_add
            if current_tab_name == "Hinzufügen"
            else self.marken_combobox_remove
        )
        categories_combobox = (
            self.categories_combobox_add
            if current_tab_name == "Hinzufügen"
            else self.categories_combobox_remove
        )
        print(f"Current Tab Name is: {current_tab_name}, id: {id(current_tab_name)}")
        print(
            f"articles_input field currently contains: >{articles_input.text()}<, id: {id(articles_input)}"
        )
        print(
            f"marken_combobox current text: {marken_combobox.currentText()}, id: {id(marken_combobox)}"
        )
        print(
            f"categories_combobox current text: {categories_combobox.currentText()}, id: {id(categories_combobox)}"
        )
        task_type = (
            "process_articles"
            if current_tab_name == "Hinzufügen"
            else "remove_articles_images"
        )

        task = {
            "task_type": task_type,
            "schedule_datetime": self.get_scheduled_time().isoformat(),
            "data": {
                "marke": marken_combobox.currentText(),
                "kategorie": categories_combobox.currentText(),
                "article_numbers": articles_input.text(),
                "img1_url": (
                    self.img1_input.text() if current_tab_name == "Hinzufügen" else None
                ),
                "img2_url": (
                    self.img2_input.text() if current_tab_name == "Hinzufügen" else None
                ),
                "width": (
                    self.width_input.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "height": (
                    self.height_input.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_checkbox": (
                    self.link_checkbox.isChecked()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_input_de": (
                    self.link_input_de.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_input_fr": (
                    self.link_input_fr.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
            },
            "follow_up": self.multi_mode,
        }
        print(f"Task created: {task}")
        return task

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

    def hide_datetime_fields(self):
        self.display_label_title.hide()
        self.datetime_label.hide()
        for widget in self.datetime_widgets:
            widget.hide()

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

    def save_task_temporarily(self):
        print("save_task_temporarily called")
        task = self.create_task()
        self.temp_tasks.append(task)
        print(f"Added task to temp_tasks: {self.temp_tasks}")
        print(f"len(self.temp_tasks) = {len(self.temp_tasks)}")
        self.clear_input_fields()
        print("Clear Input fields called")
        if len(self.temp_tasks) == 1:
            self.banner_label.setText(
                "<b>Multi-Task Mode</b>" + "<br>" + "Nach dem ersten Task ausführen"
            )
        # Show the new top banner
        self.show_confirmation_banner()
        self.update_ui_elements()

    def schedule_in_task_scheduler(self, task_filename, schedule_datetime):
        import subprocess

        date_str = schedule_datetime.strftime("%d/%m/%Y")
        time_str = schedule_datetime.strftime("%H:%M")
        command = f'SchTasks /Create /SC ONCE /TN "ButtonizerTask_{os.path.basename(task_filename)}" /TR "python {os.path.abspath(__file__).replace("bAUTOnizer3000.py", "exe_tasks.py")} {task_filename}" /ST {time_str} /SD {date_str} /F'
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to schedule task: {e}")

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

    @QtCore.pyqtProperty(QColor)
    def borderColor(self):
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color):
        self._borderColor = color
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(
            QPen(self.borderColor, 15)
        )  # Set pen with the current border color and width
        painter.drawRect(self.rect())  # Draw the border around the window

    def show_confirmation_banner(self, message="TASK ERSTELLT"):
        # Create the animation for the border
        self.border_animation = QPropertyAnimation(self, b"borderColor")
        self.border_animation.setDuration(
            500
        )  # Duration of the animation in milliseconds
        self.border_animation.setLoopCount(
            1
        )  # Number of times the animation should loop
        self.border_animation.setStartValue(
            QColor(60, 143, 64, 0)
        )  # Start with transparent green
        self.border_animation.setKeyValueAt(
            0.5, QColor(60, 143, 64, 190)
        )  # Fully opaque green at midpoint
        self.border_animation.setEndValue(
            QColor(60, 143, 64, 0)
        )  # End with transparent green
        self.border_animation.setEasingCurve(
            QEasingCurve.Type.InOutQuad
        )  # Smooth easing curve
        self.border_animation.start()
        self.top_banner_label.setStyleSheet("color: rgb(60, 143, 64);")
        self.top_banner_label.setText(f"<b>{message}</b>")
        self.top_banner_label.show()

    def get_scheduled_time(self):
        return datetime.datetime(
            self.selected_date.year(),
            self.selected_date.month(),
            self.selected_date.day(),
            self.selected_time.hour(),
            self.selected_time.minute(),
            self.selected_time.second(),
        )

    def show_datetime_fields(self):
        self.display_label_title.show()
        self.datetime_label.show()
        for widget in self.datetime_widgets:
            widget.show()

    def show_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Geschafft")
        msg_box.setText(
            "Task erfolgreich geplant. \nDu siehst heute übrigens mal wieder super aus <3"
        )
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def toggle_link_input(self, state, link_input_de, link_input_fr):
        if state == Qt.CheckState.Checked:
            link_input_de.setDisabled(False)
            link_input_fr.setDisabled(False)
        else:
            link_input_de.setDisabled(True)
            link_input_fr.setDisabled(True)

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
                    (
                        self.marken_combobox_add
                        if tab_name == "Hinzufügen"
                        else self.marken_combobox_remove
                    ),
                    (
                        self.categories_combobox_add
                        if tab_name == "Hinzufügen"
                        else self.categories_combobox_remove
                    ),
                    (
                        self.articles_input_add
                        if tab_name == "Hinzufügen"
                        else self.articles_input_remove
                    ),
                    tab_name,
                ),
            )
            button_layout.addWidget(submit_button)

    def update_datetime_label(self):
        selected_date = self.selected_date.toString("dd/MM/yyyy")
        selected_time = self.selected_time.toString("HH:mm:ss")
        self.datetime_label.setText(f"{selected_date} \n{selected_time}")

    def update_subcategories(self, marken_combobox, categories_combobox):
        selected_marke = marken_combobox.currentText()
        categories_combobox.clear()
        if selected_marke in self.category_data["Kamerasysteme + Objektive"]:
            categories_combobox.addItems(
                self.category_data["Kamerasysteme + Objektive"][selected_marke].keys()
            )

    def update_ui_elements(self):
        if self.multi_mode and len(self.temp_tasks) == 0:
            self.show_datetime_fields()
        elif self.multi_mode and len(self.temp_tasks) > 0:
            self.hide_datetime_fields()
        else:
            self.show_datetime_fields()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
