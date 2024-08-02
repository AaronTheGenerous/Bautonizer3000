"""
### bAUTOnizer3000

Script for automatic processing of promotional banner images on Webshop

©Aaron Hafner
GraphicArt AG
31.07.2024

---

### class: DatePickerDialog

QDialog subclass that provides a dialog for selecting a date using a QCalendarWidget.

#### Methods:
- __init__(parent=None)
  Initializes the DatePickerDialog with an optional parent widget. Creates the layout and sets the window title. Creates a QCalendarWidget and adds it to the layout. Calls the create_buttons method.

- create_buttons()
  Creates and adds OK and Abbrechen buttons to the layout, each with a corresponding click handler (accept/reject).

- create_button(text, handler)
  Creates a QPushButton with the given text and click handler. Returns the created button.

- get_date()
  Returns the currently selected date from the QCalendarWidget.

---

### class: TimePickerDialog

Dialog window for selecting time.

#### Methods:
- __init__(parent=None)
  Initializes the TimePickerDialog object.

- create_buttons()
  Creates the buttons in the dialog.

- create_button(text, handler)
  Creates a button with the given text and handler function.

- get_time()
  Retrieves the selected time from the time edit widget.

---

### class: App

This class represents an application window for the Buttonizer3000 program.

#### Methods:
- __init__
  Initializes the App object.
- initUI
  Initializes the user interface of the application.
- add_datetime_fields
  Adds the date and time selection fields to the UI.
- add_articles_input
  Adds the articles input fields to the specified layout.
- add_image_and_link_fields
  Adds the image and link input fields to the specified layout.
- on_articles_input_changed(text)
  Handles the event when the articles input field is changed.
- add_marken_and_categories(layout, tab_type)
  Add marken and categories input fields to the given layout based on the tab type.
- on_marken_combobox_changed(text)
  Handle the event when the marken_combobox is changed.
- on_categories_combobox_changed(text)
  Handle the event when the categories_combobox is changed.
- center_on_screen
  Centers the window on the screen based on the dimensions of the window.
- clear_input_fields
  Clears the input fields based on the current tab.
- clear_layout(layout)
  Clears all the widgets in the layout.
- create_button(text, click_handler)
  Creates a button with the specified text and click handler.
- create_label(text, font_size, alignment, with_border=False)
  Creates a QLabel with the specified text, font size, alignment, and border style.
- create_label_and_combobox(label_text, items)
  Creates a QLabel and a QComboBox with the specified label text and items.
- create_line_edit_with_label(label_text, layout)
  Creates a line edit widget with the specified label text and adds it to the layout.
- create_mode_switch(layout)
  Creates a mode switch widget with two radio buttons: "Single-Task Mode" and "Multi-Task Mode".
- create_tab(tab_name, tab_type)
  Creates a tab widget with specified name and type.
- add_task_counter(layout)
  Adds a task counter to the given layout.
- create_task
  Creates a task based on the current state of the GUI.
- eventFilter(obj, event)
  Filters events for a given object and responds to specific events.
- hide_datetime_fields
  Hides the datetime fields.
- open_date_picker
  Opens a date picker dialog and stores the selected date in self.selected_date.
- open_time_picker
  Opens a time picker dialog and retrieves the selected time.
- save_all_tasks
  Save all tasks to the specified tasks directory.
- save_task_temporarily
  Save a task temporarily.
- schedule_in_task_scheduler(task_filename, schedule_datetime)
  Schedules a task in the Task Scheduler using the SchTasks command line tool.
- schedule_task
  Schedule a task.
- paintEvent(event)
  Handles the paint event for the window.
- show_confirmation_banner(message="TASK ERSTELLT")
  Displays a confirmation banner with an optional message.
- get_scheduled_time
  Returns the scheduled time based on the selected date and time.
- show_datetime_fields
  Shows the datetime fields.
- show_message
  Shows a message box with a success message and an information icon.
- toggle_link_input(state, link_input_de, link_input_fr)
  Enables or disables the given link inputs based on the given state.
- toggle_multi_mode
  Toggles the multi mode of the application.
- update_buttons(tab_name)
  Updates the buttons in the specified tab.
- update_datetime_label
  Update the datetime label with selected date and time.
- update_subcategories(marken_combobox, categories_combobox)
  Updates the subcategories in the categories_combobox based on the selected_marke in marken_combobox.
- update_ui_elements
  Update the UI elements based on the current state.
- update_layouts
  Update layouts and widgets.
  """

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
    """

    :class: DatePickerDialog

    QDialog subclass that provides a dialog for selecting a date using a QCalendarWidget.

    Constructor: :meth: __init__(parent=None) Initializes the DatePickerDialog with an optional parent widget.
    Creates the layout and sets the window title. Creates a QCalendarWidget and adds it to the layout. Calls the
    create_buttons method.

    Methods: :meth: create_buttons() Creates and adds OK and Abbrechen buttons to the layout, each with a
    corresponding click handler (accept/reject).

        :meth: create_button(text, handler)
            Creates a QPushButton with the given text and click handler. Returns the created button.

        :meth: get_date()
            Returns the currently selected date from the QCalendarWidget.

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Datum wählen")
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.layout.addWidget(self.calendar)
        self.create_buttons()

    def create_buttons(self):
        """
        Create buttons and add them to the layout.

        :return: None
        """
        buttons = QHBoxLayout()
        buttons.addWidget(self.create_button("OK", self.accept))
        buttons.addWidget(self.create_button("Abbrechen", self.reject))
        self.layout.addLayout(buttons)

    # noinspection PyUnresolvedReferences
    def create_button(self, text, handler):
        """
        Create and return a QPushButton with the given text and click handler.

        :param text: The text to display on the button.
        :param handler: The function to be called when the button is clicked.
        :return: The created QPushButton object.

        """
        button = QPushButton(text, self)
        button.clicked.connect(handler)
        return button

    def get_date(self):
        """
        :return: the selected date from the calendar
        """
        return self.calendar.selectedDate()


class TimePickerDialog(QDialog):
    """
    Class TimePickerDialog

    Dialog window for selecting time.

    Methods:
        __init__(self, parent=None)
            Initializes the TimePickerDialog object.

        create_buttons(self)
            Creates the buttons in the dialog.

        create_button(self, text, handler)
            Creates a button with the given text and handler function.

        get_time(self)
            Retrieves the selected time from the time edit widget.

    Attributes:
        layout : QVBoxLayout
            The layout of the dialog window.

        time_edit : QTimeEdit
            The widget for selecting the time.

    Example usage:

    dialog = TimePickerDialog()
    if dialog.exec_() == QDialog.Accepted:
        selected_time = dialog.get_time()
        print("Selected time:", selected_time)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Uhrzeit wählen")
        self.layout = QVBoxLayout(self)
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.layout.addWidget(self.time_edit)
        self.create_buttons()

    def create_buttons(self):
        """
        Create buttons for OK and Cancel actions and add them to the layout.

        :return: None
        """
        buttons = QHBoxLayout()
        buttons.addWidget(self.create_button("OK", self.accept))
        buttons.addWidget(self.create_button("Cancel", self.reject))
        self.layout.addLayout(buttons)

    def create_button(self, text, handler):
        """
        Create a button with the given text and connect it to the provided handler.

        :param text: The text to display on the button.
        :param handler: The function to handle the button click event.
        :return: The created QPushButton instance.
        """
        button = QPushButton(text, self)
        button.clicked.connect(handler)
        return button

    def get_time(self):
        """
        Get the current time.

        :return: The current time.
        """
        return self.time_edit.time()


class App(QWidget):
    """
    This class represents an application window for the Buttonizer3000 program.

    Attributes:
        tasks_directory (str): The directory path for storing tasks.
        last_task_end_time_file (str): The file path for storing the last task end time.
        multi_mode (bool): A flag indicating if multi-mode is enabled.
        counter_added (bool): A flag indicating if the counter is added.

    Methods:
        __init__: Initializes the App object.
        initUI: Initializes the user interface of the application.
        add_datetime_fields: Adds the date and time selection fields to the UI.
        add_articles_input: Adds the articles input fields to the specified layout.
        add_image_and_link_fields: Adds the image and link input fields to the specified layout.
    """
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
        self._borderColor = QColor(
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

        self.task_counter_int = 0
        self.task_counters = {}

        self.category_data = {
            "Kamerasysteme + Objektive": {
                "Nikon"    : {
                    "Nikon Z"                 : {},
                    "Nikkor Z-Mount Objektive": {},
                    "Nikon DSLR"              : {},
                    "Nikkor F-Mount Objektive": {},
                    "Nikon Blitzgeräte"       : {},
                    "Nikon Coolpix"           : {},
                    "Nikon DSLR Zubehör"      : {},
                    "Nikon Objektivzubehör"   : {},
                },
                "Sony"     : {
                    "Sony E-Mount Kameras"        : {},
                    "Sony E-Mount Objektive"      : {},
                    "Sony E-Mount APS-C Kameras"  : {},
                    "Sony E-Mount APS-C Objektive": {},
                    "Sony E-Mount Zubehör"        : {},
                    "Sony Blitzgeräte"            : {},
                    "Sony Kompaktkameras"         : {},
                    "Sony XPERIA Smartphones"     : {},
                    "Sony A-Mount Kameras"        : {},
                    "Sony A-Mount Objektive"      : {},
                    "Sony A-Mount Zubehör"        : {},
                },
                "Phase One": {
                    "Phase One IQ Backs"                       : {},
                    "Phase One XF Camera System"               : {},
                    "Phase One XT Camera System"               : {},
                    "CPO Phase One IQ Backs für Phase One XF"  : {},
                    "CPO Phase One XF Kamerasysteme"           : {},
                    "CPO Phase One IQ Backs für Hasselblad"    : {},
                    "Phase One XF Kamerasysteme"               : {},
                    "Phase One XT Kamera und Objektive"        : {},
                    "Schneider Kreuznach Objektive (Blue Ring)": {},
                    "CPO Schneider Kreuznach Objektive"        : {},
                    "Capture One"                              : {},
                },
                "Cambo"    : {
                    "Cambo Wide RS"                : {},
                    "Cambo ACTUS"                  : {},
                    "Cambo Zubehör zu Phase One XT": {},
                    "Cambo Adapter"                : {},
                    "Cambo ACTUS DB"               : {},
                    "Cambo ACTUS-XL"               : {},
                },
                "Leica"    : {
                    "Leica M & Objektive"      : {},
                    "Leica Q"                  : {},
                    "Leica SL & Objektive"     : {},
                    "Leica S & Objektive"      : {},
                    "Leica TL / CL & Objektive": {},
                    "Leica V"                  : {},
                    "Leica X"                  : {},
                    "Leica SOFORT"             : {},
                },
            }
        }

        self.initUI()

    def initUI(self):
        """
        Initializes the UI by setting the window title, geometry, window icon, and layout.

        :return: None
        """
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
            self.create_tab("Hinzufügen", "add"), "Hinzufügen"
        )
        self.tab_widget.addTab(
            self.create_tab("Entfernen", "remove"), "Entfernen"
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

    def add_datetime_fields(self):
        """
        Adds the datetime fields to the widget.

        :return: None
        """
        if not self.datetime_fields_added:
            buttons = [
                ("Datum wählen", self.open_date_picker),
                ("Uhrzeit wählen", self.open_time_picker),
            ]
            self.datetime_buttons = []
            for text, handler in buttons:
                button = self.create_button(text, handler)
                self.datetime_layout.addWidget(button)
                self.datetime_widgets.append(button)

            self.datetime_fields_added = True

    def add_articles_input(self, layout, tab_type):
        # sourcery skip: extract-duplicate-method
        """
        Add articles input widget to the given layout based on the tab type.

        :param layout: The layout to add the articles input widget to.
        :type layout: QLayout
        :param tab_type: The type of tab. Can be "add" or "remove".
        :type tab_type: str
        :return: None
        """
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
        # sourcery skip: extract-duplicate-method
        """
        :param layout: The layout in which the image and link input fields will be added.
        :return: None

        Adds image and link input fields to the given layout. The method creates several line edit fields and
        checkboxes for the user to input image URLs, image height and width, and links in both German and French
        languages. The link input fields are initially disabled and will be enabled based on the state of the link
        checkbox.

        Example usage:
            layout = QVBoxLayout()
            add_image_and_link_fields(self, layout)
            QWidget.setLayout(layout)
        """
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
        self.link_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.link_checkbox.stateChanged.connect(
            lambda state: self.toggle_link_input(
                state, self.link_input_de, self.link_input_fr
            )
        )
        layout.addWidget(self.link_checkbox)

        self.link_input_de = self.create_line_edit_with_label("Link (Deutsch)", layout)
        self.link_input_de.setEnabled(False)
        layout.addWidget(self.link_input_de)
        print(f"added link_input_de: {self.link_input_de}")

        self.link_input_fr = self.create_line_edit_with_label(
            "Link (Französisch)", layout
        )
        self.link_input_fr.setEnabled(False)
        layout.addWidget(self.link_input_fr)
        print(f"added link_input_fr: {self.link_input_fr}")

    def on_articles_input_changed(self, text):
        """
        :param text: The updated text input for articles.
        :return: None
        """
        print(f"articles_input changed: {text}")

    def add_marken_and_categories(self, layout, tab_type):
        """
        :param layout: The layout to which the labels and comboboxes will be added.
        :param tab_type: The type of tab (add or remove) for which the method is being called.
        :return: None

        This method creates and adds labels and comboboxes to the given layout based on the specified tab type.
        If the tab type is "add", it creates and adds labels and comboboxes for adding marken and categories.
        If the tab type is "remove", it creates and adds labels and comboboxes for removing marken and categories.
        It also connects the necessary signals to the appropriate slots to handle changes in the comboboxes.
        """
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
        """
        Handle the event when the marken_combobox is changed.

        :param text: The new value selected in the marken_combobox.
        :type text: str
        :return: None
        """
        print(f"marken_combobox changed: {text}")

    def on_categories_combobox_changed(self, text):
        """
        :param text: The new text value in the categories_combobox.
        :return: None
        """
        print(f"categories_combobox changed: {text}")

    def center_on_screen(self):
        """
        Centers the window on the screen based on the dimensions of the window.

        :return: None
        """
        resolution = QApplication.primaryScreen().geometry()
        x = (resolution.width() - self.window_width) // 2
        y = (resolution.height() - self.height) // 2
        self.move(x, y)

    def clear_input_fields(self):
        """
        Clears the input fields based on the current tab.

        :return: None
        """
        if not (clear_fields := self.clear_checkbox.isChecked()):
            return
        current_tab_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        if current_tab_name == "Hinzufügen":
            self.clear_add_fields()
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

    def clear_add_fields(self):
        """
        Clears all input fields in the 'add' section of the UI.

        :return: None
        """
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

    def clear_layout(self, layout):
        """
        Clears all the widgets in the layout.

        :param layout: The layout to be cleared.
        :type layout: QLayout
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_button(self, text, click_handler):
        """
        :param text: The text to be displayed on the button.
        :param click_handler: The function to be called when the button is clicked.
        :return: The created button.
        """
        button = QPushButton(text, self)
        button.clicked.connect(click_handler)
        return button

    def create_label(self, text, font_size, alignment, with_border=False):
        """

        :param text: The text to be displayed on the label.
        :param font_size: The size of the font to be used for the text.
        :param alignment: The alignment of the text within the label.
        :param with_border: Optional parameter indicating whether to add a border to the label. Defaults to False.

        :return: A QLabel object with the specified text, font size, alignment, and border style (if applicable).

        """
        label = QLabel(text, self)
        font = QFont()
        font.setPointSize(font_size)
        label.setFont(font)
        label.setAlignment(alignment)
        if with_border:
            label.setStyleSheet("border: 2px solid #ffdd00;")
        return label

    def create_label_and_combobox(self, label_text, items):
        """
        Creates a QLabel and a QComboBox with the specified label text and items.

        :param label_text: The text to be displayed on the label.
        :param items: The list of items to be added to the combo box.
        :return: A tuple containing the created QLabel and QComboBox.
        """
        label = QLabel(label_text, self)
        combobox = QComboBox(self)
        combobox.addItems(items)
        return label, combobox

    def create_line_edit_with_label(self, label_text, layout):
        """
        :param label_text: The text to be displayed on the label.
        :param layout: The layout on which the label and line edit will be added.
        :return: The line edit widget that is created.
        """
        label = QLabel(label_text, self)
        layout.addWidget(label)
        return QLineEdit(self)

    def create_mode_switch(self, layout):
        """
        :param layout: The layout in which the mode switch buttons will be added.
        :return: None

        Creates a mode switch widget with two radio buttons: "Single-Task Mode" and "Multi-Task Mode".
        The widget is added to the layout specified by the 'layout' parameter.

        The mode switch buttons are part of a QButtonGroup to ensure exclusive selection.
        By default, the "Single-Task Mode" radio button is checked.

        When the mode switch buttons are toggled, the toggle_multi_mode method is called.

        Example usage:
            layout = QVBoxLayout()
            create_mode_switch(layout)
            widget.setLayout(layout)
        """
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

    def create_tab(self, tab_name, tab_type):
        """
        :param tab_name: The name of the tab to be created
        :param tab_type: The type of the tab ("add" or "remove")
        :return: The created tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout()

        self.current_tab_name = tab_name
        print(f"Creating tab: {tab_name}, id: {id(tab_name)}")

        self.add_marken_and_categories(layout, tab_type)
        self.add_articles_input(layout, tab_type)

        if tab_type == "add":
            self.add_image_and_link_fields(layout)

        self.add_datetime_fields()

        layout.addStretch(1)

        # Add Counter for currently scheduled tasks
        self.add_task_counter(layout, tab_name)

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

    def add_task_counter(self, layout, tab_name):
        """
        :param layout: The layout for which the task counter will be added.
        :param tab_name: The name of the tab.
        :return: None

        This method is used to add a task counter to the given layout.
        """
        counter_layout = QHBoxLayout()
        task_counter_title = self.create_label(
            "<b>Erstellte Tasks: </b>", 10, Qt.AlignmentFlag.AlignCenter, True
        )
        task_counter = self.create_label("<b>0</b>", 10, Qt.AlignmentFlag.AlignCenter, True)

        counter_layout.addWidget(task_counter_title)
        counter_layout.addWidget(task_counter)
        task_counter_title.setVisible(False)
        task_counter.setVisible(False)
        layout.addLayout(counter_layout)

        self.task_counters[tab_name] = (task_counter_title, task_counter)

    def create_task(self):
        """
        Method to create a task based on the current state of the GUI.

        :return: The created task as a dictionary.
        """
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
            "task_type"        : task_type,
            "schedule_datetime": self.get_scheduled_time().isoformat(),
            "data"             : {
                "marke"          : marken_combobox.currentText(),
                "kategorie"      : categories_combobox.currentText(),
                "article_numbers": articles_input.text(),
                "img1_url"       : (
                    self.img1_input.text() if current_tab_name == "Hinzufügen" else None
                ),
                "img2_url"       : (
                    self.img2_input.text() if current_tab_name == "Hinzufügen" else None
                ),
                "width"          : (
                    self.width_input.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "height"         : (
                    self.height_input.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_checkbox"  : (
                    self.link_checkbox.isChecked()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_input_de"  : (
                    self.link_input_de.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
                "link_input_fr"  : (
                    self.link_input_fr.text()
                    if current_tab_name == "Hinzufügen"
                    else None
                ),
            },
            "follow_up"        : self.multi_mode,
        }
        print(f"Task created: {task}")
        return task

    def eventFilter(self, obj, event):
        """
        Filters events for a given object and responds to specific events.

        :param obj: The object being filtered.
        :param event: The event to be filtered.

        :return: True if the event has been handled, False otherwise.

        """
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
        """
        Hides the datetime fields.

        :return: None
        """
        self.display_label_title.hide()
        self.datetime_label.hide()
        for widget in self.datetime_widgets:
            widget.hide()

    def open_date_picker(self):
        """
        Opens a date picker dialog and stores the selected date in self.selected_date.
        The method also updates the datetime label.

        :return: None
        """
        dialog = DatePickerDialog(self)
        if dialog.exec():
            self.selected_date = dialog.get_date()
            self.update_datetime_label()

    def open_time_picker(self):
        """
        Opens a time picker dialog and retrieves the selected time.

        :return: None
        """
        dialog = TimePickerDialog(self)
        if dialog.exec():
            self.selected_time = dialog.get_time()
            self.update_datetime_label()

    def save_all_tasks(self):
        """
        Save all tasks to the specified tasks directory.

        :return: None
        """
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
        self.task_counter_int = 0
        self.show_message()

    def save_task_temporarily(self):
        """
        Save a task temporarily.

        :return: None
        """
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
        self.task_counter_int += 1
        for task_counter_title, task_counter in self.task_counters.values():
            task_counter.setText(str(self.task_counter_int))

        # Show the new top banner
        self.show_confirmation_banner()
        self.update_ui_elements()

    def schedule_in_task_scheduler(self, task_filename, schedule_datetime):
        """
        :param task_filename: The filename of the task to be scheduled in the Task Scheduler.
        :param schedule_datetime: The datetime object representing the date and time when the task should be scheduled.
        :return: None

        This method schedules a task in the Task Scheduler by using the `SchTasks` command line tool. It creates a
        one-time scheduled task with a specified task name, task file, and schedule date and time.

        The `task_filename` parameter should be the filename of the task that needs to be scheduled in the Task
        Scheduler.

        The `schedule_datetime` parameter should be a datetime object representing the date and time when the task
        should be scheduled.

        This method does not return any value.
        """
        import subprocess

        date_str = schedule_datetime.strftime("%d/%m/%Y")
        time_str = schedule_datetime.strftime("%H:%M")
        command = f'SchTasks /Create /SC ONCE /TN "ButtonizerTask_{os.path.basename(task_filename)}" /TR "python {os.path.abspath(__file__).replace("bAUTOnizer3000.py", "exe_tasks.py")} {task_filename}" /ST {time_str} /SD {date_str} /F'
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to schedule task: {e}")

    def schedule_task(self):
        """
        Schedule a task.

        :return: None
        """
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
        """
        Retrieves the value of the `borderColor` property.

        :return: The color of the border.
        :rtype: QColor
        """
        return self._borderColor

    @borderColor.setter
    def borderColor(self, color):
        self._borderColor = color
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        """
        Handles the paint event for the window.

        :param event: the paint event object containing event details
        :type event: QPaintEvent
        :return: None
        """
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(
            QPen(self.borderColor, 15)
        )  # Set pen with the current border color and width
        painter.drawRect(self.rect())  # Draw the border around the window

    def show_confirmation_banner(self, message="TASK ERSTELLT"):
        """
        :param message: Optional message for the confirmation banner. Default value is "TASK ERSTELLT".
        :return: None

        This method displays a confirmation banner with an optional message. The banner contains an animated border
        that fades in and out, and a label with the specified message.

        Example usage:
            show_confirmation_banner("Task created successfully")
        """
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
        self.top_banner_label.setStyleSheet("color: rgb(60, 143, 64);")
        self.top_banner_label.setText(f"<b>{message}</b>")
        self.top_banner_label.show()

    def get_scheduled_time(self):
        """
        Returns the scheduled time based on the selected date and time.

        :return: The scheduled time.
        :rtype: datetime.datetime
        """
        return datetime.datetime(
            self.selected_date.year(),
            self.selected_date.month(),
            self.selected_date.day(),
            self.selected_time.hour(),
            self.selected_time.minute(),
            self.selected_time.second(),
        )

    def show_datetime_fields(self):
        """
        Shows the datetime fields.

        :return: None
        """
        self.display_label_title.show()
        self.datetime_label.show()
        for widget in self.datetime_widgets:
            widget.show()

    def show_message(self):
        """
        Shows a message box with a success message and an information icon.

        :return: None
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Geschafft")
        msg_box.setText(
            "Task erfolgreich geplant. \nDu siehst heute übrigens mal wieder super aus <3"
        )
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def toggle_link_input(self, state, link_input_de, link_input_fr):

        """
        Enables or disables the given link inputs based on the given state.

        :param state: The state to check. Should be one of Qt.CheckState.Checked or Qt.CheckState.Unchecked.
        :type state: int
        :param link_input_de: The link input for the German language.
        :type link_input_de: QtWidgets.QLineEdit
        :param link_input_fr: The link input for the French language.
        :type link_input_fr: QtWidgets.QLineEdit
        :return: None
        """
        print(f"toggle_link_input called with parameters: \n- State: {state} \n- link_input_de: {link_input_de} \n- "
              f"link_input_fr: {link_input_fr}")
        if state == Qt.CheckState.Checked:
            link_input_de.setEnabled(True)
            print(f"enabled link_input_de: {link_input_de}")
            print(f"link_input_de enabled status: {link_input_de.isEnabled()}")
            print(link_input_de.parent().isEnabled())
            link_input_fr.setEnabled(True)
            print(f"link_input_fr enabled status: {link_input_fr.isEnabled()}")
            print(link_input_fr.parent().isEnabled())
        else:
            link_input_de.setEnabled(False)
            print(f"link_input_de enabled status: {link_input_de.isEnabled()}")
            print(link_input_de.parent().isEnabled())
            link_input_fr.setEnabled(False)
            print(f"link_input_fr enabled status: {link_input_fr.isEnabled()}")
            print(link_input_fr.parent().isEnabled())

        # force update elements
        link_input_de.update()
        link_input_fr.update()

        QApplication.processEvents()

    def toggle_multi_mode(self):
        """
        Toggles the multi mode of the application.

        :return: None
        """
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

        show_counters = self.multi_mode
        for task_counter_title, task_counter in self.task_counters.values():
            task_counter_title.setVisible(show_counters)
            task_counter.setVisible(show_counters)

        for tab_name in self.button_layouts:
            self.update_buttons(tab_name)
        self.update_ui_elements()

    def update_buttons(self, tab_name):
        """
        Updates the buttons in the specified tab.

        :param tab_name: The name of the tab.
        :return: None
        """
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
                ),
            )
            button_layout.addWidget(submit_button)

    def update_datetime_label(self):
        """
        Update the datetime label with selected date and time.

        :return: None
        """
        selected_date = self.selected_date.toString("dd/MM/yyyy")
        selected_time = self.selected_time.toString("HH:mm:ss")
        self.datetime_label.setText(f"{selected_date} \n{selected_time}")

    def update_subcategories(self, marken_combobox, categories_combobox):
        """
        Updates the subcategories in the categories_combobox based on the selected_marke in marken_combobox.

        :param marken_combobox: The combobox representing the selected brand.
        :type marken_combobox: QComboBox
        :param categories_combobox: The combobox to be updated with subcategories.
        :type categories_combobox: QComboBox
        :return: None
        :rtype: None
        """
        selected_marke = marken_combobox.currentText()
        categories_combobox.clear()
        if selected_marke in self.category_data["Kamerasysteme + Objektive"]:
            categories_combobox.addItems(
                self.category_data["Kamerasysteme + Objektive"][selected_marke].keys()
            )

    def update_ui_elements(self):
        """
        Update the UI elements based on the current state.

        :return: None
        """
        if self.multi_mode and len(self.temp_tasks) == 0:
            self.show_datetime_fields()
        elif self.multi_mode and len(self.temp_tasks) > 0:
            self.hide_datetime_fields()
        else:
            self.show_datetime_fields()

    def update_layouts(self):
        """
        Update layouts and widgets.

        :return: None
        """
        # Force update parent layouts
        self.task_counter.updateGeometry()
        self.task_counter_title.updateGeometry()
        self.layout().update()
        self.update()
        self.repaint()
        print("Layouts and widgets updated")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
