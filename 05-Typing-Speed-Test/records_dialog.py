from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem


class RecordsDialog(QDialog):
    def __init__(self, records_data):
        super().__init__()
        self.setWindowTitle("High Scores")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        # Create a table to show Name and Score
        self.table = QTableWidget(len(records_data), 2)
        self.table.setHorizontalHeaderLabels(["Name", "WPM"])

        # Populate the table
        for row, (name, score) in enumerate(records_data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(name)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{score:.2f}"))

        layout.addWidget(self.table)