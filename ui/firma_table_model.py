# ui/firma_table_model.py
from PyQt6.QtCore import QAbstractTableModel, Qt

from models.firma import Firma


class FirmaTableModel(QAbstractTableModel):
    COLUMNS = ["ID", "Име", "Мејл", "Телефон", "Статус"]

    def __init__(self, firmi: list[Firma] | None = None):
        super().__init__()
        self._firmi: list[Firma] = firmi or []

    def set_firmi(self, firmi: list[Firma]):
        self.beginResetModel()
        self._firmi = firmi
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._firmi)

    def columnCount(self, parent=None):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        firma = self._firmi[index.row()]
        col = index.column()
        if col == 0:
            return str(firma.firma_id)
        if col == 1:
            return firma.ime
        if col == 2:
            return firma.contactMail
        if col == 3:
            return firma.contactNumber
        if col == 4:
            return firma.status
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return str(section + 1)

    def firma_id_at(self, row: int) -> int:
        return self._firmi[row].firma_id
