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
        self.resize(1400, 700)  # Подобра големина

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
        lbl_firmi.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        lbl_firmi.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.tblFirmi = QTableView()
        self.firmaModel = FirmaTableModel([])
        self.tblFirmi.setModel(self.firmaModel)
        self.tblFirmi.horizontalHeader().setStretchLastSection(True)  # Авто растојание
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
        lbl_nastani.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        lbl_nastani.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.tblNastani = QTableView()
        self.nastanModel = NastanTableModel([])
        self.tblNastani.setModel(self.nastanModel)
        self.tblNastani.horizontalHeader().setStretchLastSection(True)

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
        try:
            firmi = self.firma_service.list_firmi()
            self.firmaModel.set_firmi(firmi)
            self.nastanModel.set_nastani([])
            print(f"🔄 Loaded {len(firmi)} фирми")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Не можам да ги вчитам фирмите:\n{str(e)}")

    def on_firma_selected(self, selected, _deselected):
        self.load_nastani_for_selected_firma()

    def load_nastani_for_selected_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            self.nastanModel.set_nastani([])
            return
        try:
            nastani = self.nastan_service.list_nastani(firma_id=firma_id)
            self.nastanModel.set_nastani(nastani)
            print(f"🔄 Loaded {len(nastani)} настани за фирма {firma_id}")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Не можам да ги вчитам настаните:\n{str(e)}")

    def on_add_firma(self):
        dlg = FirmiFormDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if not data["ime"]:
                QMessageBox.warning(self, "Грешка", "Името е задолжително.")
                return
            
            try:
                firma = self.firma_service.get_or_create_firma(
                    ime=data["ime"],
                    contactMail=data.get("contactMail"),
                    contactNumber=data.get("contactNumber"),
                    opis=data.get("opis"),
                    status=data.get("status"),
                    notes=data.get("notes")
                )
                self.load_firmi()
                QMessageBox.information(self, "Успех", f"Фирма '{data['ime']}' зачувана!")
            except Exception as e:
                QMessageBox.critical(self, "Грешка", f"Не можам да ја зачувам фирмата:\n{str(e)}")

    def on_edit_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Избери фирма.")
            return
        try:
            firma = self.firma_service.get_firma(firma_id)
            if not firma:
                QMessageBox.warning(self, "Грешка", "Фирмата не постои.")
                return
            dlg = FirmiFormDialog(self, firma=firma)
            if dlg.exec():
                data = dlg.get_data()
                self.firma_service.update_firma(firma_id, **data)
                self.load_firmi()
                QMessageBox.information(self, "Успех", "Фирмата е ажурирана!")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Грешка при уредување:\n{str(e)}")

    def on_delete_firma(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Избери фирма.")
            return
        try:
            firma = self.firma_service.get_firma(firma_id)
            if QMessageBox.question(self, "Потврда", 
                f"Сигурни сте дека сакате да ја избришете фирмата?\n'{firma.ime}'") != QMessageBox.StandardButton.Yes:
                return
            ok = self.firma_service.delete_firma(firma_id)
            if not ok:
                QMessageBox.warning(self, "Грешка", "Бришењето не успеа.")
            else:
                self.load_firmi()
                QMessageBox.information(self, "Успех", "Фирмата е избришана!")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Грешка при бришење:\n{str(e)}")

    def on_add_nastan(self):
        firma_id = self._selected_firma_id()
        if not firma_id:
            QMessageBox.warning(self, "Инфо", "Прво избери фирма.")
            return
        try:
            dlg = NastanFormDialog(self)
            if dlg.exec():
                data = dlg.get_data()
                data["firma_id"] = firma_id
                if not data["ime_nastan"]:
                    QMessageBox.warning(self, "Грешка", "Името на настанот е задолжително.")
                    return
                self.nastan_service.create_nastan(**data)
                self.load_nastani_for_selected_firma()
                QMessageBox.information(self, "Успех", "Настанот е зачуван!")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Не можам да го зачувам настанот:\n{str(e)}")

    def on_edit_nastan(self):
        nastan_id = self._selected_nastan_id()
        if not nastan_id:
            QMessageBox.warning(self, "Инфо", "Избери настан.")
            return
        try:
            nastan = self.nastan_service.get_nastan(nastan_id)
            if not nastan:
                QMessageBox.warning(self, "Грешка", "Настанот не постои.")
                return
            dlg = NastanFormDialog(self, nastan=nastan)
            if dlg.exec():
                data = dlg.get_data()
                self.nastan_service.update_nastan(nastan_id, **data)
                self.load_nastani_for_selected_firma()
                QMessageBox.information(self, "Успех", "Настанот е ажуриран!")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Грешка при уредување:\n{str(e)}")

    def on_delete_nastan(self):
        nastan_id = self._selected_nastan_id()
        if not nastan_id:
            QMessageBox.warning(self, "Инфо", "Избери настан.")
            return
        try:
            nastan = self.nastan_service.get_nastan(nastan_id)
            if QMessageBox.question(self, "Потврда", 
                f"Сигурни сте дека сакате да го избришете настанот?\n'{nastan.ime_nastan}'") != QMessageBox.StandardButton.Yes:
                return
            ok = self.nastan_service.delete_nastan(nastan_id)
            if not ok:
                QMessageBox.warning(self, "Грешка", "Бришењето не успеа.")
            else:
                self.load_nastani_for_selected_firma()
                QMessageBox.information(self, "Успех", "Настанот е избришан!")
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Грешка при бришење:\n{str(e)}")
