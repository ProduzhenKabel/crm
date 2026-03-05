# ui/firmi_form.py
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QTextEdit

from models.firma import Firma


class FirmiFormDialog(QDialog):
    def __init__(self, parent=None, firma: Firma | None = None):
        super().__init__(parent)
        self.setWindowTitle("Фирма")
        self._firma = firma

        self.imeEdit = QLineEdit()
        self.contactMailEdit = QLineEdit()
        self.contactNumberEdit = QLineEdit()
        self.opisEdit = QTextEdit()
        self.statusEdit = QLineEdit()
        self.notesEdit = QTextEdit()

        form = QFormLayout()
        form.addRow("Име:", self.imeEdit)
        form.addRow("Мејл:", self.contactMailEdit)
        form.addRow("Телефон:", self.contactNumberEdit)
        form.addRow("Опис:", self.opisEdit)
        form.addRow("Статус:", self.statusEdit)
        form.addRow("Белешки:", self.notesEdit)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        form.addRow(self.buttons)
        self.setLayout(form)

        if firma:
            self._load_firma(firma)

    def _load_firma(self, firma: Firma):
        self.imeEdit.setText(firma.ime or "")
        self.contactMailEdit.setText(firma.contactMail or "")
        self.contactNumberEdit.setText(firma.contactNumber or "")
        self.opisEdit.setPlainText(firma.opis or "")
        self.statusEdit.setText(firma.status or "")
        self.notesEdit.setPlainText(firma.notes or "")

    def get_data(self) -> dict:
        return {
            "ime": self.imeEdit.text().strip(),
            "contactMail": self.contactMailEdit.text().strip() or None,
            "contactNumber": self.contactNumberEdit.text().strip() or None,
            "opis": self.opisEdit.toPlainText().strip() or None,
            "status": self.statusEdit.text().strip() or None,
            "notes": self.notesEdit.toPlainText().strip() or None,
        }
