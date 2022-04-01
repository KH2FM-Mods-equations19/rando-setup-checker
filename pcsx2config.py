from PySide6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QFileDialog, QLabel, QVBoxLayout, QTextEdit

import validation
from randoconfig import Pcsx2RandoConfiguration, path_or_none


class Pcsx2ConfigurationDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PCSX2 Configuration')
        self.setMinimumWidth(800)

        grid = QGridLayout()

        openkh_path_field = QLineEdit()
        openkh_path_field.setToolTip('Contains various tools from the OpenKH project such as the OpenKH Mods Manager')
        self.openkh_path_field = openkh_path_field
        openkh_path_button = QPushButton('Choose')
        openkh_path_button.clicked.connect(self._choose_openkh_path)
        grid.addWidget(QLabel('OpenKH Location'), 0, 0, 1, 2)
        grid.addWidget(openkh_path_field, 1, 0)
        grid.addWidget(openkh_path_button, 1, 1)

        cheats_path_field = QLineEdit()
        cheats_path_field.setToolTip('Contains .pnach files used to mod the game')
        self.cheats_path_field = cheats_path_field
        cheats_path_button = QPushButton('Choose')
        cheats_path_button.clicked.connect(self._choose_cheats_path)
        grid.addWidget(QLabel('Cheats Location'), 2, 0, 1, 2)
        grid.addWidget(cheats_path_field, 3, 0)
        grid.addWidget(cheats_path_button, 3, 1)

        validate = QPushButton('Check Configuration')
        validate.clicked.connect(self._validate_clicked)

        validation_result = QTextEdit()
        validation_result.setReadOnly(True)
        self.validation_result = validation_result

        box = QVBoxLayout()
        box.addLayout(grid)
        box.addWidget(validate)
        box.addWidget(validation_result)
        self.setLayout(box)

    def _choose_openkh_path(self):
        output = QFileDialog.getExistingDirectory()
        if output is not None and output != '':
            self.openkh_path_field.setText(output)

    def _choose_cheats_path(self):
        output = QFileDialog.getExistingDirectory()
        if output is not None and output != '':
            self.cheats_path_field.setText(output)

    def _validate_clicked(self):
        rando_configuration = Pcsx2RandoConfiguration.read(
            openkh_path=path_or_none(self.openkh_path_field.text()),
            cheats_path=path_or_none(self.cheats_path_field.text())
        )
        all_results = rando_configuration.validate_all()
        validation.show_validation_result(self.validation_result, all_results)
