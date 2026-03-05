# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QMessageBox,
    QLabel,
)
from PyQt6.QtCore import Qt

from services.firma_service import FirmaService
from services.nastan_service import NastanService
from ui.firma_table_model import FirmaTableModel
from ui.nastan_table_model import NastanTableModel
from ui.firmi_form import FirmiFormDialog
from ui.nastan_form import NastanFormDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Firmi и Настани")

        self.firma_service = FirmaService()
        self.nastan_service = NastanService()

        self._build_ui()
        self.load_firmi()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # Left: Firmi
        left_layout = QVBoxLayout()
        lbl_firmi = QLabel("Фирми")
        self.tblFirmi = QTableView()
        self.firmaModel = FirmaTableModel([])
        self.tblFirmi.setModel(self.firmaModel)
        self.tblFirmi.selectionModel().selectionChanged.connect(self.on_firma_selected)

        btn_add_firma = QPushButton("Додади фирма")
        btn_edit_firma = QPushButton("Измени фирма")
        btn_del_firma = QPushButton("Избриши фирма")
        btn_refresh_firma = QPushButton("Освежи")

        btn_add_firma.clicked.connect(self.on_add_firma)
        btn_edit_firma.clicked.connect(self.on_edit_firma)
        btn_del_firma.clicked.connect(self.on_delete_firma)
        btn_refresh_firma.clicked.connect(self.load_firmi)

        left_layout.addWidget(lbl_firmi)
        left_layout.addWidget(self.tblFirmi)
        left_btns = QHBoxLayout()
        left_btns.addWidget(btn_add_firma)
        left_btns.addWidget(btn_edit_firma)
        left_btns.addWidget(btn_del_firma)
        left_btns.addWidget(btn_refresh_firma)
        left_layout.addLayout(left_btns)

        # Right: Nastani
        right_layout = QVBoxLayout()
        lbl_nastani = QLabel("Настани (за избрана фирма)")
        self.tblNastani = QTableView()
        self.nastanModel = NastanTableModel([])
        self.tblNastani.setModel(self.nastanModel)

        btn_add_nastan = QPushButton("Додади настан")
        btn_edit_nastan = QPushButton("Измени настан")
        btn_del_nastan = QPushButton("Избриши настан")
        btn_refresh_nastan = QPushButton("Освежи")

        btn_add_nastan.clicked.connect(self.on_add_nastan)
        btn_edit_nastan.clicked.connect(self.on_edit_nastan)
        btn_del_nastan.clicked.connect(self.on_delete_nastan)
        btn_refresh_nastan.clicked.connect(self.load_nastani_for_selected_firma)

        right_layout.addWidget(lbl_nastani)
        right_layout.addWidget(self.tblNastani)
        right_btns = QHBoxLayout()
        right_btns.addWidget(btn_add_nastan)
        right_btns.addWidget(btn_edit_nastan)
        right_btns.addWidget(btn_del_nastan)
        right_btns.addWidget(btn_refresh_nastan)
        right_layout.addLayout(right_btns)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

    def _selected_firma_id(self) -> int | None:
        index = self.tblFirmi.currentIndex()
        if not index.isValid():
            return None
        return self.firmaModel.firma_id_at(index.row())

    def _selected_nastan_id(self) -> int | None:
        index = self.tblNastani.currentIndex()
        if not index.isValid():
            return None
        return self.nastanModel.nastan_id_at(index.row())

    def load_firmi(self):
        firmi = self.firma_service.list_firmi()
        self.firmaModel.set_firmi(firmi)
        self.nastanModel.set_nastani([])

    def on_firma_selected(self, selected, _deselected):
        self.load_nastani_for_selected_firma()

    def load_nastani_for_selected_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            self.nastanModel.set_nastani([])
            return
        nastani = self.nastan_service.list_nastani(firma_id=firma_id)
        self.nastanModel.set_nastani(nastani)

    def on_add_firma(self):
        dlg = FirmiFormDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if not data["ime"]:
                QMessageBox.warning(self, "Грешка", "Името е задолжително.")
                return
            self.firma_service.create_firma(**data)
            self.load_firmi()

    def on_edit_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Избери фирма.")
            return
        firma = self.firma_service.get_firma(firma_id)
        if not firma:
            QMessageBox.warning(self, "Грешка", "Фирмата не постои.")
            return
        dlg = FirmiFormDialog(self, firma=firma)
        if dlg.exec():
            data = dlg.get_data()
            self.firma_service.update_firma(firma_id, **data)
            self.load_firmi()

    def on_delete_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Избери фирма.")
            return
        if QMessageBox.question(self, "Потврда", "Сигурни сте дека сакате да ја избришете фирмата?") \
                != QMessageBox.StandardButton.Yes:
            return
        ok = self.firma_service.delete_firma(firma_id)
        if not ok:
            QMessageBox.warning(self, "Грешка", "Бришењето не успеа.")
        self.load_firmi()

    def on_add_nastan(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Прво избери фирма.")
            return
        dlg = NastanFormDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            data["firma_id"] = firma_id
            if not data["ime_nastan"]:
                QMessageBox.warning(self, "Грешка", "Името на настанот е задолжително.")
                return
            self.nastan_service.create_nastan(**data)
            self.load_nastani_for_selected_firma()

    def on_edit_nastan(self):
        nastan_id = self._selected_nastan_id()
        if not nastan_id:
            QMessageBox.warning(self, "Инфо", "Избери настан.")
            return
        nastan = self.nastan_service.get_nastan(nastan_id)
        if not nastan:
            QMessageBox.warning(self, "Грешка", "Настанот не постои.")
            return
        dlg = NastanFormDialog(self, nastan=nastan)
        if dlg.exec():
            data = dlg.get_data()
            self.nastan_service.update_nastan(nastan_id, **data)
            self.load_nastani_for_selected_firma()

    def on_delete_nastan(self):
        nastan_id = self._selected_nastan_id()
        if not nastan_id:
            QMessageBox.warning(self, "Инфо", "Избери настан.")
            return
        if QMessageBox.question(self, "Потврда", "Сигурни сте дека сакате да го избришете настанот?") \
                != QMessageBox.StandardButton.Yes:
            return
        ok = self.nastan_service.delete_nastan(nastan_id)
        if not ok:
            QMessageBox.warning(self, "Грешка", "Бришењето не успеа.")
        self.load_nastani_for_selected_firma()
