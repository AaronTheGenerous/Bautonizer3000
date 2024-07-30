# Add Counter for currently scheduled tasks
self.counter_layout = QHBoxLayout()
self.task_counter_title = self.create_label(
    "Erstellte Tasks: ", 15, Qt.AlignmentFlag.AlignCenter, True
)
self.task_counter = self.create_label("", 15, Qt.AlignmentFlag.AlignCenter, True)
self.counter_layout.addWidget(self.task_counter_title)
self.counter_layout.addWidget(self.task_counter)
self.datetime_layout.addLayout(self.counter_layout)
