# ui/nastan_table_model.py
from PyQt6.QtCore import QAbstractTableModel, Qt

from models.nastan import Nastan


class NastanTableModel(QAbstractTableModel):
    COLUMNS = ["ID", "Име настан", "Датум", "Ишод"]

    def __init__(self, nastani: list[Nastan] | None = None):
        super().__init__()
        self._nastani: list[Nastan] = nastani or []

    def set_nastani(self, nastani: list[Nastan]):
        self.beginResetModel()
        self._nastani = nastani
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._nastani)

    def columnCount(self, parent=None):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        nastan = self._nastani[index.row()]
        col = index.column()
        if col == 0:
            return str(nastan.nastan_id)
        if col == 1:
            return nastan.ime_nastan
        if col == 2:
            return str(nastan.data)
        if col == 3:
            return nastan.ishod
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return str(section + 1)

    def nastan_id_at(self, row: int) -> int:
        return self._nastani[row].nastan_id
