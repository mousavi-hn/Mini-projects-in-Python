from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView


class RecordsDialog(QDialog):
    def __init__(self, records_data):
        super().__init__()
        self.setWindowTitle("High Scores")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        items = sorted(records_data.items(), key=lambda x: x[1], reverse=True)
        self.table = QTableWidget(len(items), 2)
        self.table.setHorizontalHeaderLabels(["Name", "Score"])

        for row, (name, score) in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(name)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{score}"))

        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)