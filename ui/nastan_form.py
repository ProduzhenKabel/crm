# ui/nastan_form.py
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QDateEdit,
)
from PyQt6.QtCore import QDate

from models.nastan import Nastan


class NastanFormDialog(QDialog):
    def __init__(self, parent=None, nastan: Nastan | None = None):
        super().__init__(parent)
        self.setWindowTitle("Настан")
        self._nastan = nastan

        self.imeNastanEdit = QLineEdit()
        self.dataEdit = QDateEdit(QDate.currentDate())
        self.opisEdit = QTextEdit()
        self.ishodEdit = QLineEdit()

        form = QFormLayout()
        form.addRow("Име настан:", self.imeNastanEdit)
        form.addRow("Датум:", self.dataEdit)
        form.addRow("Опис:", self.opisEdit)
        form.addRow("Исход:", self.ishodEdit)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        form.addRow(self.buttons)
        self.setLayout(form)

        if nastan:
            self._load_nastan(nastan)

    def _load_nastan(self, nastan: Nastan):
        self.imeNastanEdit.setText(nastan.ime_nastan or "")
        if nastan.data:
            self.dataEdit.setDate(QDate.fromString(str(nastan.data), "yyyy-MM-dd"))
        self.opisEdit.setPlainText(nastan.opis or "")
        self.ishodEdit.setText(nastan.ishod or "")

    def get_data(self) -> dict:
        return {
            "ime_nastan": self.imeNastanEdit.text().strip(),
            "data": self.dataEdit.date().toPyDate(),
            "opis": self.opisEdit.toPlainText().strip() or None,
            "ishod": self.ishodEdit.text().strip() or None,
        }
